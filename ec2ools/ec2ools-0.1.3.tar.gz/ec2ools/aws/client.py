import boto3
import subprocess



class Client:

    _boto_clients = {}


    def __init__(self, client, **kw):
        self.region = kw.get('region', self._get_region())
        return self._client(name)


    def _get_region(self):
        cmd = "curl http://169.254.169.254/latest/dynamic/instance-identity/document|grep region|awk -F\" '{print $4}'"
        res = subprocess.check_output(cmd)
        return res

    def _client(self, name):
        """ Create and cache boto3 client
        """
        if not self._boto_clients.get(self.region).get(name):
            client = boto3.client(name, region_name=self.region)
            if not self._boto_clients.get(self.region):
                self._boto_clients[self.region] = {}
            self._boto_clients[self.region_name][name] = client

        return self._boto_clients[self.region][name]


class MetaData:

    @classmethod
    def get(cls, name):
        """
        """
        arg = "--{}".format(name)

        cmd = "ec2-metadata {}".format(arg)

        try:
            return subprocess.check_output(cmd)
        except Exception as e:
            print(str(e))
