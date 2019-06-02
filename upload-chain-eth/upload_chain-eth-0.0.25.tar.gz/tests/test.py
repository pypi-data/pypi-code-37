#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from upload_chain.database.db import *


# def test():
#     logger.info("xxxxxxx")


if __name__ == "__main__":
    # test()
    # logger.info("my test.")
    # logger.error("my test.")
    # create_person(name='yuyongpeng')
    # query_person(name='cat')
    # key = query_keys('6bS8KmBtE1Rs5Eg')
    # logger.info(key.address)

    str1 = 'testing '
    str2 = 'string '
    str3 = 'concation '
    # str = ''.join([str1, str2, str3])
    # print(str)
    str = b'\n    {"type":"call_function","notice":["database"],"send_database":{"mysql":{"schema":"cport","sql":{"success":["update person_dc set \n\t\t\t\t\t\t\t\tperson_hash = \'0xa76f7182126655eb214c2424cff76a052d43d0be76d17bd5dbd49c421a1c6190\',\n\t\t\t\t\t\t\t\tperson_address = \'0xbAb2c6c16A35b5889B272f96fe5400dbd8368952\',\n\t\t\t\t\t\t\t\tstatus = 3 where id = 1","update person set auth = 2 where person_id = 45 and auth = 1"],"fail":["update person_dc set status = 2 where id = 1"]}}},"function":{"name":"setAttributeSigned","args":[{"name":"identity","value":"0xbAb2c6c16A35b5889B272f96fe5400dbd8368952","type":"address"},{"name":"sigV","value":"1c","source_type":"hex","type":"uint8"},{"name":"sigR","value":"67ecffb19da5dc8f88ebca58fcf1d116ac78a16330a9ddd74527c3b7be84baba","source_type":"hex","type":"bytes32"},{"name":"sigS","value":"2002e5ba7d48f1e5112fbaa4f6fe00271dabe74e36ce1d823818e14eba0ef072","source_type":"hex","type":"bytes32"},{"name":"name","value":"\xe5\xa3\xab\xe5\x85\xb5","type":"bytes32"},{"name":"value","value":"{"@context":"https://w3id.org/did/v1","id":"did:ethr:bAb2c6c16A35b5889B272f96fe5400dbd8368952#soldier","publicKey":[{"id":"did:ethr:bAb2c6c16A35b5889B272f96fe5400dbd8368952#soldier","type":"EciesVerificationKey","controller":"did:ethr:bAb2c6c16A35b5889B272f96fe5400dbd8368952","publicKeyHex":"0x041f2157ca4c8c1d7008dccd733b6e9519d1be4b0e8099b1d9d0d84cd37b94d789534ad7d2770664a4ae81fc2ba168f769d9be59e30d73a533f5f17758d2ef4966"}],"authentication":[{"id":"did:ethr:DeCD6626f23bc43cB4D738cB0F2Dde922D691fD2#soldier","type":"EciesVerificationKey","controller":"did:ethr:DeCD6626f23bc43cB4D738cB0F2Dde922D691fD2","publicKeyHex":"0x044af3c4d907a75e9349f362b0f854c7d74a89dad457df4f9cbf3c4f9e2f7fbcf8916ac219bb70e64777930b1e85d0a550e1e61ca94fa902dee419849a9a0efe8a"}],"proof":"d5b4e3e8c64c1827bbe7043fd3974c304b45233d8d405143851b115ab0500c7acd9dee760e3a73ba67218a3fc4e1ad84","created":1559457904740}\n17c6d9776541603bf782f476dd0447ee11347028d4b7c1e78b2e2e7fc61cf1cb30f60da8c81cd784396fa2d20533e12ffc1ef1835f03693649a33aa82be3922e01","type":"bytes"}]}}\n    '
    str2 = b'\n    {"type":"call_function","notice":["database"],"send_database":{"mysql":{"schema":"cport","sql":{"success":["update person_dc set \n\t\t\t\t\t\t\t\tperson_hash = \'0xa76f7182126655eb214c2424cff76a052d43d0be76d17bd5dbd49c421a1c6190\',\n\t\t\t\t\t\t\t\tperson_address = \'0xbAb2c6c16A35b5889B272f96fe5400dbd8368952\',\n\t\t\t\t\t\t\t\tstatus = 3 where id = 1","update person set auth = 2 where person_id = 45 and auth = 1"],"fail":["update person_dc set status = 2 where id = 1"]}}}}\n    '
    str3 = b'\n    {"type":"call_function","notice":["database"],"send_database":{"mysql":{"schema":"cport","sql":{"success":["update person_dc set x"]}}}}\n    '
    import json
    obj = json.loads(str3.strip().decode('utf8'))
    print(obj)


class Generator(object):

    def __init__(self, name):
        self.name = name

    def __enter__(self):
        print("There's no way out")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
          # 检查退出的类型
        # 当有异常发生时 exc_type存在值
        if exc_type:
            print('Open the door')
        else:
            print('100%')

    def generate(self):
        print('%s can uses love to generate electricity' % self.name)

# 紧跟with后面的语句被求值后，返回对象的 `__enter__() `方法被调用,
# 这个方法的返回值将被赋值给as后面的变量
with Generator("LEX") as lex:
    lex.generate()
# 当with后面的代码块全部被执行完之后，将调用返回对象的 `__exit__()`方法。

from contextlib import contextmanager
@contextmanager
def opening(filename):
    f = open(filename)  # IOError is untouched by GeneratorContext
    try:
        yield f
    finally:
        f.close()  # Ditto for errors here (however unlikely)

class MyFunc(object):
    """实现上下文管理器"""

    def __init__(self, file_name, mode):
        self.file_name = file_name
        self.mode = mode

    def __enter__(self):
        self.f_obj = open(self.file_name, self.mode)
        return self.f_obj          # __enter__函数返回的是打开资源的对象

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.f_obj.close()


with open("file_name", "r") as file_obj:
    content = file_obj.read()

print(content)

from datetime import datetime
unix_ts = 1509636585.0
times = datetime.fromtimestamp(unix_ts)
a = times.strftime("%Y-%m-%d %H:%M:%S")