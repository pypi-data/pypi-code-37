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

class Asr:
    def __init__(self, url, corpId, authKey):
        # ASR URL
        self.uri = url +  '?corp_id=' + corpId + '&auth_key=' + authKey 

    def stt(self, senderId, filepath, language):
        # language: Cantonese, English, Mandarin
        returnObj = {}
        data = {
            'input_language': 'cantonese',
            'require_diarization': 'False'
        }
        files = {
            'speech': open(filepath, 'rb')
        }
        response = requests.post(self.uri + '&user_id=' + senderId,data=data,files=files,verify=False)
        if response.status_code != 200:
            print('ASR error code is %s' % response.status_code)
            returnObj['status'] = response.status_code
            returnObj['statusText'] = response.reason
            returnObj['error_msg'] = json.loads(response.text)['error_msg']
        else:
            response_json = response.json()
            status = response_json.get('ok')
            if status != True:
                print('ASR returns error %s' % status)
            else:
                # ASR returns json
                print('ASR result: %s' % response_json)
                returnObj['status'] = 200
                returnObj['content'] = response_json.get('result').get('outputs')
        return returnObj