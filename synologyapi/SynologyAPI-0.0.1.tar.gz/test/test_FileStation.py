#!/usr/bin/python3
# 2019-05-07
# Daniel Nicolas Gisolfi

import os
import json
import pytest
from src.filestation import FileStation

class TestAuth:
    fileStation = FileStation(
        'danielgisolfi',
        'nagcu3-cixkyz-xobhEm',
        'https://share.ecrl.marist.edu:5001'
    )

    # Test if the account can upload files
    # to the url
    def testUploadFile(self):
        response = self.fileStation.uploadFile(f'{os.getcwd()}/test/test.txt', '/HoneypotLogs/HoneynetLogs')
        assert response.status_code == 200

        response_json = json.loads(response.content)

        success = response_json['success']
        assert success == True
        
        file = response_json['data']['file']
        assert file == 'test.txt'
