from typing import Dict

import boto3
import rapidjson


class Bullhorn:
    def __init__(self, topic_map: Dict[str, str], client=None):
        if not client:
            client = boto3.client('sns')
        self._client = client
        self._topic_map = topic_map

    @classmethod
    def retrieve(cls, resource=None, profile=None):
        topic_map = {}
        if not resource:
            resource = boto3.resource('sns')
            if profile:
                resource = boto3.Session(profile_name=profile).resource('sns')
        topic_iterator = resource.topics.all()
        for entry in topic_iterator:
            attributes = entry.attributes
            topic_arn = attributes['TopicArn']
            display_name = attributes['DisplayName']
            if display_name:
                topic_map[display_name] = topic_arn
        client = boto3.client('sns')
        if profile:
            client = boto3.Session(profile_name=profile).client('sns')
        return cls(topic_map, client)

    @property
    def topic_map(self):
        return self._topic_map

    def publish_task(self,  task_name, flow_id, task_kwargs):
        msg = {
            'task_name': task_name,
            'flow_id': flow_id,
            'task_kwargs': task_kwargs
        }
        topic_arn = self._topic_map.get(task_name)
        if topic_arn is None:
            raise RuntimeError(f'there is no listener available for task_name: {task_name}')
        return self._publish('new_event', topic_arn, rapidjson.dumps(msg))

    def _publish(self, message_subject, topic_arn, message_body):
        response = self._client.publish(
            TopicArn=topic_arn,
            Subject=message_subject,
            Message=message_body
        )
        return response['MessageId']
