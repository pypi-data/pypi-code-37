#!/usr/bin/env python
#-*- coding:utf-8 -*-

from accobot import Accobot

class Chatbot:

    def __init__(self):
        self.client = Accobot('https://acdev.fanoai.cn/chat?user_id=', 'default@fano.ai', 'fanolabs', 'TD1')

    def __call__(self, senderId, text, language):
        return self.client.chat(senderId, text, language)
 
def main():
    returnObj = Chatbot()('test_henry', 'hello', 'cantonese')
    print(returnObj)
 
if __name__ == '__main__':
    main()