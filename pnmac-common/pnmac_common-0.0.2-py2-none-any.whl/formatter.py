import json

def safe_to_json(str_or_dict):
    if type(str_or_dict) in [unicode, str]:
        return json.loads(str_or_dict)
    elif type(str_or_dict) == dict:
        return str_or_dict
    else:
        raise Exception("Unsupported type %s" % type(str_or_dict))
