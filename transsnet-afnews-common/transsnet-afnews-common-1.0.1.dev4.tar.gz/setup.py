from setuptools import find_packages
from setuptools import setup

setup(
    name='transsnet-afnews-common',  # 包名字
    version='1.0.1.dev4',  # 包版本（每次需要更新这个再推到git上）
    description='python common utils for transsnet africa news',  # 简单描述
    url='https://git.ms.netease.com/africaNews/python-common',  # 包的主页
    packages=find_packages(where='.', exclude=(), include=('*',)),  # 部署的包，这里就是搜索所有的包含__init__.py的目录
    install_requires=[
        'redis',
        'redis-py-cluster'
    ]  # 需要的依赖， 后面可以跟 ">1.0" 表示需要的最小版本号
)
