from longan_sqlite import *

# 初始化Longan，指定数据库地址
# debug为true，则打印所有sql语句
Longan.init('test.db', debug=True)

# 指定某张表实例化longan
longan = Longan('OrderData')

# 执行sql文件
longan.execute_file('test.sql')

longan.insert_or_update(Flesh(OrderName="x", GroupId=1, LogDone=3))

for r in longan.query():
    print(r)

longan.insert_or_update(Flesh(OrderName="y", GroupId=2, LogDone=3))
longan.insert_or_update(Flesh(OrderName="z", GroupId=3, LogDone=10))
for r in longan.query():
    print(r)