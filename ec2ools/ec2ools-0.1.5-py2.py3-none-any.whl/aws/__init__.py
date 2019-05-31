import boto3
import subprocess
import shlex
import json

EC2_METADATA='/usr/bin/ec2-metadata'
REGION=None

def client(name, region=None):
    """
    """
    if not region:
        region = get_region()
    return boto3.client(name, region_name=region)


def get_region():
    """ Get region from metadata
        and cache value in global
        constant
    """
    global REGION
    if REGION is None:
        cmd = "curl -s http://169.254.169.254/latest/dynamic/instance-identity/document"
        res = subprocess.check_output(shlex.split(cmd))
        REGION= json.loads(res)['region']
    return REGION


def metadata(name):
    """
    """
    arg = "--{}".format(name)

    cmd = "{} {}".format(EC2_METADATA, arg)

    try:
        res = subprocess.check_output(shlex.split(cmd))
        return res.decode().split(":")[1].strip()
    except Exception as e:
        print(str(e))
