class JRDBData:
    def __init__(self, filename, schema_type, yymmdd, records):
        self.filename = filename
        self.schema_type = schema_type
        self.yymmdd = yymmdd
        self.records = records
