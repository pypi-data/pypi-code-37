import abc
from collections import Iterable
from copy import deepcopy
from .DomainEventListener import (
    DomainEventListener,
    ApplicationDomainEventPublisher,
)
from .DomainObject import DomainObject
from pymongo import MongoClient
import pymysql.cursors
import json
from itertools import zip_longest


class Repository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def load(self, object_id):
        raise NotImplementedError()

    @abc.abstractmethod
    def exists(self, object_id):
        raise NotImplementedError()

    @abc.abstractmethod
    def save(self, obj):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_event_stream_for(self, object_id):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_event_stream_since(self, event_id):
        raise NotImplementedError()

    @abc.abstractmethod
    def max_version_for_object(self, object_id):
        raise NotImplementedError()

    @abc.abstractmethod
    def create_blank_domain_object(self):
        raise NotImplementedError()

    @staticmethod
    def merge_event_streams(prioritary_event_stream, other_event_stream):
        """Merge two event streams and manage possible conflit.

        Conflicts in event stream are event streams with repeating event number

        If there is a conflit, the first stream is considered prioritary.
        The conflict is then resolved by appending the additional elements of the second stream
        after these from the first. Events numbers are then correctly modified

        Requires:
            The two event streams are for the same object_id

        Returns:
            The merged event stream

        """

        diff1, diff2 = DomainObject.diff_event_streams(
            prioritary_event_stream, other_event_stream
        )

        if len(diff1) == 0 and len(diff2) == 0:
            return prioritary_event_stream
        elif len(diff1) == 0 and len(diff2) != 0:
            return other_event_stream
        elif len(diff1) != 0 and len(diff2) == 0:
            return prioritary_event_stream
        else:
            result_stream = deepcopy(prioritary_event_stream)
            actual_version = result_stream[-1]["version"] + 1
            for event in diff2:
                event["version"] = actual_version
                actual_version += 1
                result_stream.append(event)
            return result_stream


class EventPublisherRepository(Repository, metaclass=abc.ABCMeta):
    def __init__(self):
        self.listeners = list()
        self.register_listener(ApplicationDomainEventPublisher().instance)

    def save(self, obj):
        to_emit = self.append_to_stream(obj)

        assert to_emit is not None
        assert isinstance(to_emit, Iterable)

        for event in to_emit:
            for listener in self.listeners:
                assert isinstance(listener, DomainEventListener)
                listener.domainEventPublished(event)

    def register_listener(self, listener):
        assert listener is not None
        assert isinstance(listener, DomainEventListener)

        if listener not in self.listeners:
            self.listeners.append(listener)

    @abc.abstractmethod
    def append_to_stream(self, obj):
        raise NotImplementedError()


class MongoEventSourceRepository(
    EventPublisherRepository, metaclass=abc.ABCMeta
):
    def __init__(
        self,
        host="localhost",
        port=27017,
        database="fenrys",
        collection="event_store",
    ):
        super().__init__()
        self.__client = MongoClient(host, port)
        self.__db = self.__client[database]
        self.__collection = self.__db[collection]

    def append_to_stream(self, obj):
        assert obj is not None
        assert isinstance(obj, DomainObject)

        max_known_version = self.max_version_for_object(obj.object_id)
        merged_stream = self.merge_event_streams(
            self.get_event_stream_for(obj.object_id), obj.event_stream
        )
        merged_stream_version = merged_stream[-1]["version"]

        events_to_add = list()
        if merged_stream_version > max_known_version:
            for event in filter(
                lambda e: e["version"] > max_known_version, merged_stream
            ):
                events_to_add.append(deepcopy(event))

        if len(events_to_add) > 0:
            self.__collection.insert_many(events_to_add)

        return deepcopy(events_to_add)

    def load(self, object_id):
        obj = self.create_blank_domain_object()
        assert isinstance(obj, DomainObject)

        stream = self.get_event_stream_for(object_id)
        obj.rehydrate(stream)

        return obj

    def exists(self, object_id):
        return self.__collection.count_documents({"object_id": object_id}) > 0

    def get_event_stream_for(self, object_id):
        return list(
            self.__collection.find({"object_id": object_id}, {"_id": 0})
        )

    def max_version_for_object(self, object_id):
        max_version_event = list(
            self.__collection.find({"object_id": object_id})
            .sort([("version", -1)])
            .limit(1)
        )

        if len(max_version_event) == 0:
            return 0
        else:
            return max_version_event[0]["version"]

    def get_event_stream_since(self, event_id):
        event = self.__collection.find_one({"event_id": event_id})
        event_timestamp = event["event_timestamp"]
        events_iterator = self.__collection.find(
            {"event_timestamp": {"$gte": event_timestamp}}
        ).sort([("event_timestamp", 1)])

        for event in events_iterator:
            yield event


class MySQLSourceRepository(EventPublisherRepository, metaclass=abc.ABCMeta):

    __CREATE_STREAM = """create table `{}`(`object_id` varchar(255) not null, `version` int not null, `event_name` varchar(255) not null, `event` longtext not null, `event_timestamp` double not null, primary key(`object_id`, `version`))"""
    __SELECT_OBJECT_STREAM = "select * from `{}` where object_id = %s"
    __INSERT_OBJECT_STREAM = "insert into `{}`(`object_id`, `version`, `event_name`, `event`, `event_timestamp`) values(%s, %s, %s, %s, %s)"
    __CHECK_TABLE_EXISTS = "show tables like %s"
    __TABLE_EXISTS = False

    def __init__(
        self,
        user="fenrys",
        password="fenrys",
        host="localhost",
        database="fenrys",
        table="event_store",
    ):
        super().__init__()
        self.__connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=database,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )
        self.__table = table

        self.__create_table()

    def __del__(self):
        self.__connection.close()

    def __create_table(self):
        if not self.__table_exists():
            try:
                with self.__connection.cursor() as cursor:
                    cursor.execute(
                        MySQLSourceRepository.__CREATE_STREAM.format(
                            self.__table
                        )
                    )
                self.__connection.commit()
            except Exception as e:
                self.__connection.rollback()
                raise e

    def __table_exists(self):
        if not MySQLSourceRepository.__TABLE_EXISTS:
            with self.__connection.cursor() as cursor:
                cursor.execute(
                    MySQLSourceRepository.__CHECK_TABLE_EXISTS, (self.__table)
                )
                result = cursor.fetchone()
                if result:
                    MySQLSourceRepository.__TABLE_EXISTS = True
                    return True
                else:
                    return False
        else:
            return True

    def append_to_stream(self, obj):
        assert obj is not None
        assert isinstance(obj, DomainObject)

        max_known_version = self.max_version_for_object(obj.object_id)

        events_to_add = list()
        if obj.version_number > max_known_version:
            for event in obj.event_stream:
                if event["version"] > max_known_version:
                    events_to_add.append(deepcopy(event))

        if len(events_to_add) > 0:
            try:
                with self.__connection.cursor() as cursor:
                    cursor.executemany(
                        MySQLSourceRepository.__INSERT_OBJECT_STREAM.format(
                            self.__table
                        ),
                        map(
                            lambda event: (
                                event["object_id"],
                                int(event["version"]),
                                event["event_name"],
                                json.dumps(event["event"]),
                                "{:10.15f}".format(
                                    float(event["event_timestamp"])
                                ),
                            ),
                            events_to_add,
                        ),
                    )
                self.__connection.commit()
            except Exception as e:
                self.__connection.rollback()
                raise e

        return deepcopy(events_to_add)

    def load(self, object_id):
        obj = self.create_blank_domain_object()
        assert isinstance(obj, DomainObject)

        stream = self.get_event_stream_for(object_id)
        obj.rehydrate(stream)

        return obj

    def exists(self, object_id):
        return len(self.get_event_stream_for(object_id)) > 0

    def get_event_stream_for(self, object_id):
        stream = list()

        with self.__connection.cursor() as cursor:
            cursor.execute(
                MySQLSourceRepository.__SELECT_OBJECT_STREAM.format(
                    self.__table
                ),
                (object_id),
            )
            results = cursor.fetchall()
            for result in results:
                r = dict()
                r["object_id"] = result["object_id"]
                r["version"] = int(result["version"])
                r["event_name"] = result["event_name"]
                r["event"] = json.loads(result["event"])
                r["event_timestamp"] = float(result["event_timestamp"])
                stream.append(r)

        return stream

    def max_version_for_object(self, object_id):
        stream = self.get_event_stream_for(object_id)

        return (
            max(map(lambda x: x["version"], stream)) if len(stream) > 0 else 0
        )


class InMemoryEventSourceRepository(
    EventPublisherRepository, metaclass=abc.ABCMeta
):
    def __init__(self):
        super().__init__()
        self.__repo = list()

    def append_to_stream(self, obj):
        assert obj is not None
        assert isinstance(obj, DomainObject)

        max_known_version = self.max_version_for_object(obj.object_id)
        merged_stream = self.merge_event_streams(
            self.get_event_stream_for(obj.object_id), obj.event_stream
        )
        merged_stream_version = merged_stream[-1]["version"]

        events_to_add = list()
        if merged_stream_version > max_known_version:
            for event in merged_stream:
                if event["version"] > max_known_version:
                    events_to_add.append(event)
                    self.__repo.append(event)

        return deepcopy(events_to_add)

    def load(self, object_id):
        obj = self.create_blank_domain_object()
        assert isinstance(obj, DomainObject)

        stream = self.get_event_stream_for(object_id)
        obj.rehydrate(stream)

        return obj

    def exists(self, object_id):
        return len(self.get_event_stream_for(object_id)) > 0

    def get_event_stream_for(self, object_id):
        stream = list()
        for event in self.__repo:
            if event["object_id"] == object_id:
                stream.append(event)
        return stream

    def get_event_stream_since(self, event_id):
        ignore = True
        for event in sorted(self.__repo, key=lambda x: x["event_timestamp"]):
            if event["event_id"] == event_id:
                ignore = False

            if not ignore:
                yield event

    def max_version_for_object(self, object_id):
        max_known_version = 0
        stream = self.get_event_stream_for(object_id)

        for event in stream:
            if event["version"] > max_known_version:
                max_known_version = event["version"]

        return max_known_version
