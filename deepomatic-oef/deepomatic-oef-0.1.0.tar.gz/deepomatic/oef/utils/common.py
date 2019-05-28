import sys
from google.protobuf import json_format
from deepomatic.api.client import Client
from thoth import logger, VERSION

# ###############################################################################

if sys.version_info >= (3, 0):
    def is_string(x):
        return isinstance(x, str)
else:
    def is_string(x):
        return isinstance(x, basestring)

# ###############################################################################


def parse_protobuf_from_json_or_binary(protobuf_class, data):
    if sys.version_info >= (3, 0):
        is_ascii = all(c < 128 for c in data)
    else:
        is_ascii = all(ord(c) < 128 for c in data)

    if is_ascii:
        try:
            return json_format.Parse(data, protobuf_class())
        except json_format.ParseError as e:
            logger.info("Failed to load the protobuf from JSON (Got: {}). Trying to load it as a binary.".format(str(e)))
    msg = protobuf_class()
    msg.ParseFromString(data)
    return msg


def new_api_client(app_id=None, api_key=None):
    return Client(app_id, api_key, user_agent_suffix='thoth/{}'.format(VERSION))
