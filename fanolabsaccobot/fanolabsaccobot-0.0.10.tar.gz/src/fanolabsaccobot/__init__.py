# -*- coding: utf-8 -*-

########################################################################
#  
# FANO LABS CONFIDENTIAL 
# __________________ 
#  
# [2017] - [2019] Fano Labs Limited 
# All Rights Reserved. 
#  
# NOTICE: All information contained herein is, and remains 
# the property of Fano Labs Limited and its suppliers, 
# if any. The intellectual and technical concepts contained 
# herein are proprietary to Fano Labs Limited 
# and its suppliers and may be covered by Hong Kong and Foreign Patents, 
# patents in process, and are protected by trade secret or copyright law. 
# Dissemination of this information or reproduction of this material 
# is strictly forbidden unless prior written permission is obtained 
# from Fano Labs Limited. 
#

import requests
import json
import base64

class Accobot:
    def __init__(self, url, userName, password, scope):
        # Accobot URL
        self.uri = url
        # Generate base64 authorization
        self.base64BasicAuth = 'Basic ' + base64.b64encode((userName+':'+password).encode(encoding="utf-8")).decode()
        self.headers={
            'Content-Type': 'application/json',
            'scope': scope,
            'rejectUnauthorized': 'false',
            'Authorization': self.base64BasicAuth,
            'product': 'accobot'
        }

    def chat(self, senderId, text, language):
        # language: mandarin / cantonese / english-usa
        returnObj = {}
        data = {
            'content_type': 'text/plain',
            'input_language': language,
            'content': text
        }
        response = requests.post(self.uri + senderId,data=json.dumps(data),headers=self.headers,verify=False)
        if response.status_code != 200:
            print('Accobot error code is %s' % response.status_code)
            returnObj['status'] = response.status_code
            returnObj['statusText'] = response.reason
            returnObj['error_msg'] = json.loads(response.text)['error_msg']
        else:
            response_json = response.json()
            status = response_json.get('status')
            if status != 'success':
                print('Accobot returns error %s' % status)
            else:
                # Accobot returns json
                print('Accobot result: %s' % response_json)
                returnObj['status'] = 200
                returnObj['content'] = response_json.get('content')
        return returnObj