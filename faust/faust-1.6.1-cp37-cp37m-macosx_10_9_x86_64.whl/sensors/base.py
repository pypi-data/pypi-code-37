"""Base-interface for sensors."""
from time import monotonic
from typing import Any, Dict, Iterator, Mapping, Optional, Set

from mode import Service

from faust.types import AppT, CollectionT, EventT, StreamT
from faust.types.assignor import PartitionAssignorT
from faust.types.tuples import Message, PendingMessage, RecordMetadata, TP
from faust.types.sensors import SensorDelegateT, SensorT
from faust.types.topics import TopicT
from faust.types.transports import ConsumerT, ProducerT

__all__ = ['Sensor', 'SensorDelegate']


class Sensor(SensorT, Service):
    """Base class for sensors.

    This sensor does not do anything at all, but can be subclassed
    to create new monitors.
    """

    def on_message_in(self, tp: TP, offset: int, message: Message) -> None:
        """Message received by a consumer."""
        ...

    def on_stream_event_in(self, tp: TP, offset: int, stream: StreamT,
                           event: EventT) -> Optional[Dict]:
        """Message sent to a stream as an event."""
        return None

    def on_stream_event_out(self, tp: TP, offset: int, stream: StreamT,
                            event: EventT, state: Dict = None) -> None:
        """Event was acknowledged by stream.

        Notes:
            Acknowledged means a stream finished processing the event, but
            given that multiple streams may be handling the same event,
            the message cannot be committed before all streams have
            processed it.  When all streams have acknowledged the event,
            it will go through :meth:`on_message_out` just before offsets
            are committed.
        """
        ...

    def on_message_out(self,
                       tp: TP,
                       offset: int,
                       message: Message) -> None:
        """All streams finished processing message."""
        ...

    def on_topic_buffer_full(self, topic: TopicT) -> None:
        """Topic buffer full so conductor had to wait."""
        ...

    def on_table_get(self, table: CollectionT, key: Any) -> None:
        """Key retrieved from table."""
        ...

    def on_table_set(self, table: CollectionT, key: Any, value: Any) -> None:
        """Value set for key in table."""
        ...

    def on_table_del(self, table: CollectionT, key: Any) -> None:
        """Key deleted from table."""
        ...

    def on_commit_initiated(self, consumer: ConsumerT) -> Any:
        """Consumer is about to commit topic offset."""
        ...

    def on_commit_completed(self, consumer: ConsumerT, state: Any) -> None:
        """Consumer finished committing topic offset."""
        ...

    def on_send_initiated(self, producer: ProducerT, topic: str,
                          message: PendingMessage,
                          keysize: int, valsize: int) -> Any:
        """About to send a message."""
        ...

    def on_send_completed(self,
                          producer: ProducerT,
                          state: Any,
                          metadata: RecordMetadata) -> None:
        """Message successfully sent."""
        ...

    def on_send_error(self,
                      producer: ProducerT,
                      exc: BaseException,
                      state: Any) -> None:
        """Error while sending message."""
        ...

    def on_assignment_start(self,
                            assignor: PartitionAssignorT) -> Dict:
        """Partition assignor is starting to assign partitions."""
        return {'time_start': monotonic()}

    def on_assignment_error(self,
                            assignor: PartitionAssignorT,
                            state: Dict,
                            exc: BaseException) -> None:
        ...

    def on_assignment_completed(self,
                                assignor: PartitionAssignorT,
                                state: Dict) -> None:
        """Partition assignor completed assignment."""
        ...

    def on_rebalance_start(self, app: AppT) -> Dict:
        """Cluster rebalance in progress."""
        return {'time_start': monotonic()}

    def on_rebalance_return(self, app: AppT, state: Dict) -> None:
        """Consumer replied assignment is done to broker."""
        ...

    def on_rebalance_end(self, app: AppT, state: Dict) -> None:
        """Cluster rebalance fully completed (including recovery)."""
        ...

    def asdict(self) -> Mapping:
        return {}


class SensorDelegate(SensorDelegateT):
    """A class that delegates sensor methods to a list of sensors."""

    _sensors: Set[SensorT]

    def __init__(self, app: AppT) -> None:
        self.app = app
        self._sensors = set()

    def add(self, sensor: SensorT) -> None:
        # connect beacons
        sensor.beacon = self.app.beacon.new(sensor)
        self._sensors.add(sensor)

    def remove(self, sensor: SensorT) -> None:
        self._sensors.remove(sensor)

    def __iter__(self) -> Iterator:
        return iter(self._sensors)

    def on_message_in(self, tp: TP, offset: int, message: Message) -> None:
        for sensor in self._sensors:
            sensor.on_message_in(tp, offset, message)

    def on_stream_event_in(self, tp: TP, offset: int, stream: StreamT,
                           event: EventT) -> Optional[Dict]:
        """Call when stream starts processing an event."""
        return {
            sensor: sensor.on_stream_event_in(tp, offset, stream, event)
            for sensor in self._sensors
        }

    def on_stream_event_out(self, tp: TP, offset: int, stream: StreamT,
                            event: EventT, state: Dict = None) -> None:
        """Call when stream is done processing an event."""
        sensor_state = state or {}
        for sensor in self._sensors:
            sensor.on_stream_event_out(tp, offset, stream, event,
                                       sensor_state.get(sensor))

    def on_topic_buffer_full(self, topic: TopicT) -> None:
        for sensor in self._sensors:
            sensor.on_topic_buffer_full(topic)

    def on_message_out(self,
                       tp: TP,
                       offset: int,
                       message: Message) -> None:
        for sensor in self._sensors:
            sensor.on_message_out(tp, offset, message)

    def on_table_get(self, table: CollectionT, key: Any) -> None:
        for sensor in self._sensors:
            sensor.on_table_get(table, key)

    def on_table_set(self, table: CollectionT, key: Any, value: Any) -> None:
        for sensor in self._sensors:
            sensor.on_table_set(table, key, value)

    def on_table_del(self, table: CollectionT, key: Any) -> None:
        for sensor in self._sensors:
            sensor.on_table_del(table, key)

    def on_commit_initiated(self, consumer: ConsumerT) -> Any:
        # This returns arbitrary state, so we return a map from sensor->state.
        return {
            sensor: sensor.on_commit_initiated(consumer)
            for sensor in self._sensors
        }

    def on_commit_completed(self, consumer: ConsumerT, state: Any) -> None:
        # state is now a mapping from sensor->state, so
        # make sure to correct the correct state to each sensor.
        for sensor in self._sensors:
            sensor.on_commit_completed(consumer, state[sensor])

    def on_send_initiated(self, producer: ProducerT, topic: str,
                          message: PendingMessage,
                          keysize: int, valsize: int) -> Any:
        return {
            sensor: sensor.on_send_initiated(
                producer, topic, message, keysize, valsize)
            for sensor in self._sensors
        }

    def on_send_completed(self,
                          producer: ProducerT,
                          state: Any,
                          metadata: RecordMetadata) -> None:
        for sensor in self._sensors:
            sensor.on_send_completed(producer, state[sensor], metadata)

    def on_send_error(self,
                      producer: ProducerT,
                      exc: BaseException,
                      state: Any) -> None:
        for sensor in self._sensors:
            sensor.on_send_error(producer, exc, state[sensor])

    def on_assignment_start(self,
                            assignor: PartitionAssignorT) -> Dict:
        """Partition assignor is starting to assign partitions."""
        return {
            sensor: sensor.on_assignment_start(assignor)
            for sensor in self._sensors
        }

    def on_assignment_error(self,
                            assignor: PartitionAssignorT,
                            state: Dict,
                            exc: BaseException) -> None:
        for sensor in self._sensors:
            sensor.on_assignment_error(assignor, state[sensor], exc)

    def on_assignment_completed(self,
                                assignor: PartitionAssignorT,
                                state: Dict) -> None:
        """Partition assignor completed assignment."""
        for sensor in self._sensors:
            sensor.on_assignment_completed(assignor, state[sensor])

    def on_rebalance_start(self, app: AppT) -> Dict:
        """Cluster rebalance in progress."""
        return {
            sensor: sensor.on_rebalance_start(app)
            for sensor in self._sensors
        }

    def on_rebalance_return(self, app: AppT, state: Dict) -> None:
        """Consumer replied assignment is done to broker."""
        for sensor in self._sensors:
            sensor.on_rebalance_return(app, state[sensor])

    def on_rebalance_end(self, app: AppT, state: Dict) -> None:
        """Cluster rebalance fully completed (including recovery)."""
        for sensor in self._sensors:
            sensor.on_rebalance_end(app, state[sensor])

    def __repr__(self) -> str:
        return f'<{type(self).__name__}: {self._sensors!r}>'
