from twilio.base.exceptions import TwilioRestException


class Assistant:

    def __init__(self, unique_name, friendly_name=None, log_queries=True, callback_events=None,
                 style_sheet=None, defaults=None):
        """
        :param unique_name:
        :param friendly_name:
        :param log_queries:
        :param callback_events:
        :param style_sheet:
        :param defaults:
        """
        self.unique_name = unique_name
        self.friendly_name = friendly_name
        self.log_queries = log_queries
        self.callback_events = callback_events
        self.style_sheet = style_sheet
        self.defaults = defaults

    def fetch_or_create(self, twilio_client):
        """
        If an assistant exists then update the assistant with the current parameters and return it.  If the
        assistant does not exist then create it based on the current values.
        :param twilio_client: A Twilio
        :return: A Twilio AssistantInstance object.
        """
        try:
            assistant = twilio_client.autopilot.assistants(self.unique_name).fetch()
            return twilio_client.autopilot.assistants(assistant.sid).update(**self.__dict__)
        except TwilioRestException:
            return twilio_client.autopilot.assistants.create(**self.__dict__)


class FieldType:

    def __init__(self, unique_name, friendly_name=None):
        self.unique_name = unique_name
        self.friendly_name = friendly_name

    def fetch_or_create(self, twilio_assistant):
        try:
            field_type = twilio_assistant.field_types(self.unique_name).fetch()
            return field_type.update(**self.__dict__)
        except TwilioRestException:
            return twilio_assistant.field_types.create(**self.__dict__)


class FieldValue:

    PROPERTIES = [
        "language",
        "value",
        "synonym_of"
    ]

    def __init__(self, language, value, synonym_of=None):
        self.language = language
        self.value = value
        self.synonym_of = synonym_of

    def fetch_or_create(self, base_resource):
        field_values = base_resource.field_values.list()

        for v in field_values:
            if v["value"] == self.value:
                return base_resource.\
                    field_values(v["sid"]).\
                    update(**self.__dict__)

        return base_resource.\
            field_values(v["sid"]).\
            create(**self.__dict__)
