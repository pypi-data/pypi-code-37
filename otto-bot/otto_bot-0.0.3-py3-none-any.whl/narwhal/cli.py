import click
import json
from click.exceptions import ClickException
from .utilities import setup_twilio_client
from .resources import Assistant, FieldType, FieldValue


@click.group()
def handler():
    pass


@handler.command()
@click.argument("config_loc")
def deploy(config_loc):
    """
    Deploys a Twilio Autopilot model based on the configuration file provided.
    :param config_loc: Location of the configuration file to deploy.
    :return:
    """
    # TODO: Verify configruation file has all required elements.

    # Setup the Twilio client with the provided authorization.
    client = setup_twilio_client()

    config = json.load(open(config_loc, "r"))

    # Start building the assistant.
    assistant = Assistant(**config["assistant"]).fetch_or_create(client)

    # Setup any custom fields that are used by the assistant.
    for ft in config.get("field_types"):
        field_type = FieldType(**ft["properties"]).fetch_or_create(assistant)

        # Add field values to the FieldType.
        for fv in ft["values"]:
            field_value = FieldValue(**fv).fetch_or_create(field_type)


@handler.command()
@click.argument("autopilot_sid")
def teardown(sid):
    """
    Tears down an Autopilot bot working through the resource hierarchy.  All resources associated with the bot
    will be deleted.
    :param sid: The unique identifier of the bot.
    :return:
    """
    pass


if __name__ == "__main__":
    handler()
    heart = "i love bean and matt time ;)"
