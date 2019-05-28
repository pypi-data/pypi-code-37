import fastavro


# class JRDBAvroWriter:
#     def __init__(self, schema):
#         self.schema = fastavro.parse_schema(schema)
#         print(self.schema)


def write(fo, schema, records: list):
    parsed_schema = fastavro.parse_schema(schema)
    fastavro.write.writer(fo, parsed_schema, records)
