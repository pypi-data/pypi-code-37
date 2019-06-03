from distutils.core import setup

setup(
    name='testsetup',  # 对外我们模块的名字
    version='1.0', # 版本号
    description='这是第一个对外发布的模块，测试哦',  #描述
    author='yema', # 作者
    author_email='madaobo198117@163.com',
    py_modules=['testsetup.猜拳','testsetup.领养宠物','testsetup.宠物（调用）'] # 要发布的模块
)