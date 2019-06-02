"""Util"""

import stringcase


def camel_case_dict(data):
    """Transform json http json response key from snake to camel case"""
    return dict((stringcase.camelcase(key), value) for key, value in data.items())
