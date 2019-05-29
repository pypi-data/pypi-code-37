"""Upload file to IBM Cloud Object Storage."""
import logging
import ibm_boto3
from ibm_botocore.client import Config, ClientError

import os
import ntpath

LOG = logging.getLogger(__name__)


class CloudObjectStorageUpload(object):  # pylint: disable=unused-variable
    """Upload a file to Cloud Object Storage."""

    command = "cos"

    def __init__(self, args, extra):
        self.args = args
        self.extra = extra
        self.session = ibm_boto3.session.Session(
            aws_access_key_id=args.access_key,
            aws_secret_access_key=args.secret_key,
            ibm_service_instance_id=args.instance_id,
        )
        self.client = self.session.client("s3", endpoint_url=args.endpoint_url)
        self.s3 = self.session.resource("s3", endpoint_url=args.endpoint_url)

    def path_leaf(self, path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

    @classmethod
    def parse_args(cls, subparsers):
        """Add Cloud Object Storage arguments to command line parser."""
        cos_oo_parser = subparsers.add_parser("cos", description=cls.__doc__)

        cos_oo_parser.add_argument(
            "-e", "--endpoint-url", help="endpoint URL of the S3 storage"
        )
        cos_oo_parser.add_argument("-s", "--instance-id", help="service instance id")
        cos_oo_parser.add_argument(
            "-u", "--access-key", help="acccess key id of HMAC credentials"
        )
        cos_oo_parser.add_argument(
            "-p", "--secret-key", help="secret access key of HMAC credentials"
        )
        cos_oo_parser.add_argument(
            "local_path",
            nargs="?",
            default=None,
            help="path in the local file system of the file to be uploaded",
        )
        cos_oo_parser.add_argument("bucket", help="target s3 bucket")
        cos_oo_parser.add_argument(
            "remote_path",
            help="""path on Cloud Object Storage where the file
                                  will be stored""",
        )

    def upload(self):
        """Upload a file from `local_path` to `remote_path` on ObjectStorage."""
        LOG.info("uploading '%s' to Cloud Object Storage", self.args.local_path)
        LOG.info(
            "target path: 's3://%s/%s' at '%s'",
            self.args.bucket,
            self.args.remote_path,
            self.args.endpoint_url,
        )

        bucket = self.s3.Bucket(self.args.bucket)

        # make sure target bucket exists
        if bucket.name not in [
            b["Name"] for b in self.client.list_buckets()["Buckets"]
        ]:
            LOG.info("bucket '%s' not found. creating it...", self.args.bucket)
            bucket.create()

        if os.path.isfile(self.args.local_path):
            bucket.upload_file(
                os.path.abspath(self.args.local_path),
                "{}/{}".format(
                    self.args.remote_path, self.path_leaf(self.args.local_path)
                ),
            )
            LOG.info("upload complete")
        else:
            LOG.info("file does not exist")
