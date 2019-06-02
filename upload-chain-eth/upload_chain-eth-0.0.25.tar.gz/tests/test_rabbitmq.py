#! /usr/bin/env python
# -*- coding: utf8 -*-
"""
Author:       yuyongpeng@hotmail.com
Github:       https://github.com/yuyongpeng/
Date:         2019-04-08 17:40:12
LastEditors:  
LastEditTime: 2019-04-08 17:40:12
Description:  
"""

import pika
from upload_chain import setting
from upload_chain.setting import VAR

def send_msg(file):
    """ 发送消息 """
    # 初始化配置信息
    setting.read_config2(file)
    # connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    credentials = pika.PlainCredentials('hard', 'chain')
    connection = pika.BlockingConnection(pika.ConnectionParameters(VAR['QUEUE_IP'], VAR['QUEUE_PORT'], VAR['QUEUE_VHOST'], credentials))
    channel = connection.channel()
    body = '''  
    {
  "type":"call_function",
  "retry": 0,                   
  "max_retry": 3,              
  "upload_timeout": 300,    
  "send_database": {
    "mysql": {
      "schema": "cport",
      "table": "person_dc",   
      "id": "123456",    
      "id_column": "id", 
      "column": "status", 
      "success_tag": "1", 
      "failed_tag": "2" 
    }
  },
  "send_email": ["yuyongpeng@hotmail.com"],
  "send_queue":{
    "queue_type": "rabbitmq",
    "queue_msg": {
      "queue_name": "cport_notice_contract"
    }
  },
  "function":{
    "name": "setAttributeSigned", 
    "args": [       
      {
        "name": "identity",  
        "value": "0xB2be7c8722935DB16921D64Ad0dDB5D47A52482a",     
        "type": "address"  
      },
      {
        "name": "sigV",
        "value": "00",
        "source_type": "hex",
        "type": "uint8"
      },
      {
        "name": "sigR",
        "value": "1bac8f2eeaf962ccf9ace9845c40f553453fb0079d80173dfcc7daf051240917",
        "source_type": "hex",
        "type": "bytes32"
      },
      {
        "name": "sigS",
        "value": "34888f4ba7b8591025fddafbba5b9e3c229a49073daeaa203d4b0260aa09b775",
        "source_type": "hex",
        "type": "bytes32"
      },
      {
        "name": "name",
        "value": "士兵",
        "type": "bytes32"
      },
      {
        "name": "value",
        "value": "{\\"@context\\":\\"https://w3id.org/did/v1\\",\\"id\\":\\"did:ethr:B2be7c8722935DB16921D64Ad0dDB5D47A52482a#soldier\\",\\"publicKey\\":[{\\"id\\":\\"did:ethr:B2be7c8722935DB16921D64Ad0dDB5D47A52482a#soldier\\",\\"type\\":\\"EciesVerificationKey\\",\\"controller\\":\\"did:ethr:B2be7c8722935DB16921D64Ad0dDB5D47A52482a\\",\\"publicKeyHex\\":\\"0x04521fbe1f862845cb09ca6c0cdff00417d4a3bf3c04748806eb49079f5d2d5d555c6461ecc3760bd10de1bc7c77421f02bbe3642d6d3e35ee219f84a026478297\\"}],\\"authentication\\":[{\\"id\\":\\"did:ethr:DeCD6626f23bc43cB4D738cB0F2Dde922D691fD2#soldier\\",\\"type\\":\\"EciesVerificationKey\\",\\"controller\\":\\"did:ethr:DeCD6626f23bc43cB4D738cB0F2Dde922D691fD2\\",\\"publicKeyHex\\":\\"0x044af3c4d907a75e9349f362b0f854c7d74a89dad457df4f9cbf3c4f9e2f7fbcf8916ac219bb70e64777930b1e85d0a550e1e61ca94fa902dee419849a9a0efe8a\\"}],\\"proof\\":\\"5a20a8ab74ba21186197c5315369dea7eb50a9700a0d88c49c360f9e3e926880b7e8f793acd91800c33c2d64ae9c846c\\",\\"created\\":1554808209789}\\nb4f2d5447a602dca239d8ab528e1cb1b0ddc409d0941700fcffed5e6bd427c2755658c7e7790a94f69417ce43c5b31c9d82e9b2900d77afcec6d4268d4e446d300",
        "type": "bytes"
      }
    ]
  }
}
    '''

    import json
    # b = json.loads(body)
    # channel.queue_delete(queue='cport_notice_contract')
    # exit(0)
    channel.queue_declare(queue=VAR['QUEUE_NAME'], durable=False)

    channel.basic_publish(exchange='',
                          routing_key=VAR['QUEUE_NAME'],
                          body=body)
    print(body)
    connection.close()


if __name__ == '__main__':
    send_msg("/Users/yuyongpeng/git/hard-chain/cport/upload_chain/upload_chain.conf")
