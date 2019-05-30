import pytest
from pytest_mock import mocker
from ec2ools.aws import client
import boto3

class TestClient:


    def test_constructor(self, mocker):

        region_mock = mocker.patch('ec2ools.aws.client.Client._get_region')
        region_mock.return_value = 'us-compton-1'

        inst = client.Client('test')

        print(inst.__dict__)


