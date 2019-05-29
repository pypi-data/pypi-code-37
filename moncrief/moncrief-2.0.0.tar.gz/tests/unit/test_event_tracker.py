import os

import pytest

from algernon.aws.task_setup import tracked_queued


@tracked_queued
def mock_function(event, context):
    return {'event': event, 'context': context}


os.environ['STATE_GQL_ENDPOINT'] = 'some_endpoint'
os.environ['DEBUG'] = 'True'


@pytest.mark.event_tracker
class TestEventTracker:
    def test_event_tracker_open_history(self, gql_client_mock, called_event, open_event_history, mock_context):
        gql_client_mock.return_value = open_event_history
        results = mock_function(called_event, mock_context)
        pass
