from google.cloud import storage
from jrdb import writer, schema
import io


class JRDBDataGCSRepo:
    def __init__(self, bucket_name):
        gcs_cli = storage.Client()
        self.bucket = gcs_cli.get_bucket(bucket_name)

    def store(self, jrdb_data):
        buf = io.BytesIO()
        writer.write(buf, schema.get(jrdb_data.schema_type), jrdb_data.records)
        blob = self.bucket.blob(
                '{}/{}.avro'.format(jrdb_data.schema_type, jrdb_data.yymmdd))
        blob.upload_from_string(buf.getvalue())
