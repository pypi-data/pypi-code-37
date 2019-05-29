from dobby.events.base.adapters.base_request_adapter import BaseRequestAdapter
from dobby.events.sns.requests.message_list_sns_request import MessageListSNSRequest


class MessageListSnsRequestAdapter(BaseRequestAdapter):
    """
        An adapter for SNS events that constructs the request using only the
        decoded bodies of the messages
    """

    __RECORDS_KEY = 'Records'

    def __init__(self):
        BaseRequestAdapter.__init__(self)

    def translate(self, event, context):

        records = event[self.__RECORDS_KEY]
        messages = list(map(
            lambda m: str(m['Sns']['Message']),
            records
        ))

        return MessageListSNSRequest(messages)
