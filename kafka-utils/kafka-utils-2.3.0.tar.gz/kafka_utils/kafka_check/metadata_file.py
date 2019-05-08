def _parse_meta_properties_file(content):
    for line in content:
        parts = line.rstrip().split("=")
        if len(parts) == 2 and parts[0] == "broker.id":
            return int(parts[1])
    return None


def _read_generated_broker_id(meta_properties_path):
    """reads broker_id from meta.properties file.

    :param string meta_properties_path: path for meta.properties file
    :returns int: broker_id from meta_properties_path
    """
    try:
        with open(meta_properties_path, 'r') as f:
            broker_id = _parse_meta_properties_file(f)
    except IOError:
        raise IOError(
            "Cannot open meta.properties file: {path}"
            .format(path=meta_properties_path),
        )
    except ValueError:
        raise ValueError("Broker id not valid")

    if broker_id is None:
        raise ValueError("Autogenerated broker id missing from data directory")

    return broker_id


def get_broker_id(data_path):
    """This function will look into the data folder to get the automatically created
    broker_id.

    :param string data_path: the path to the kafka data folder
    :returns int: the real broker_id
    """

    # Path to the meta.properties file. This is used to read the automatic broker id
    # if the given broker id is -1
    META_FILE_PATH = "{data_path}/meta.properties"

    if not data_path:
        raise ValueError("You need to specify the data_path if broker_id == -1")
    meta_properties_path = META_FILE_PATH.format(data_path=data_path)
    return _read_generated_broker_id(meta_properties_path)
