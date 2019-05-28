import os
from twilio.rest import Client
from click.exceptions import ClickException


def setup_twilio_client():
    """
    Sets up the Twilio client that will be used based on the authentication of the user.
    :return: Returns a Twilio Client object.
    """
    # TODO: Handle when Twilio authentication fails.
    try:
        account_sid = os.environ["TWILIO_ACCOUNT_SID"]
        auth_token = os.environ["TWILIO_AUTH_TOKEN"]

        client = Client(account_sid, auth_token)
    except KeyError as e:
        raise ClickException("Missing authentication environmental variable '{}'.".format(e))

    return client


def validate_configuration(config):
    """

    :param config:
    :return:
    """
    search_pattern = {
        "assistant": {
            "is_required": True,
            "required_fields": ["unique_name"]
        },
        "field_type": {
            "is_required": False,
            "required_fields": ["unique_name"]
        }
    }
    pass
