import uuid


def generate_unique_id():
    """
    Returns a unique ID using `uuid` module.
    :return: str
    """

    return uuid.uuid4().hex
