# -*- coding:utf-8 -*-
import requests
import json
class Bark:
    def __init__(self, url):
        self.url = url

    def send(self, title, content=None):
        '''title and content should not contain \'/\' character, and should be instances of unicode'''

        assert(title)
        if not isinstance(title, unicode):
            title = title.decode('utf-8')
        if not isinstance(content, unicode):
            content = content.decode('utf-8')

        message = self.url + u'/' + title + u'/'+ (content if content else u'')

        assert(message.count(u'/')== 5)
        ret = requests.get(message, {})
        ret = json.loads(ret.content)

        return True if ret['code'] == 200 else False

if __name__ == "__main__" :
    b = Bark('https://api.day.app/xgoRDhWgXCxPvEY4DDWeYQ')

