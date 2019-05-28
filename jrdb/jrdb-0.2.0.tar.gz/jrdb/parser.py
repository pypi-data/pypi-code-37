def _strip(value):
    return value.decode('cp932').strip().rstrip('\x00')


def convert(raw, schema):
    return {field['name']: _strip(raw[field['start']:field['end']])
            for field in schema['fields']}
