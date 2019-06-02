#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os, sys, shutil

py_version = sys.version_info[:2]

if py_version <= (2, 7):
    raise RuntimeError('On Python 2, Oracle not Support !')
elif (3, 0) < py_version < (3, 6):
    raise RuntimeError('On Python 3, Oracle requires Python 3.6 or later')


# copy upload_chain.conf -> /etc/upload_chain.conf
here = os.path.abspath(os.path.dirname(__file__))
shutil.copyfile(os.path.join(here, 'upload_chain.conf'), '/etc/upload_chain.conf')

try:
    README = open(os.path.join(here, 'README.md')).read()
    CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()
except:
    README = """
upload_chain 是一个智能协约的管理程序，用于导入event的数据到数据库中，和处理event数据
"""
    CHANGES = ''


setup(
    name="upload_chain-eth",
    version="0.0.25",
    author="yuyongpeng",
    author_email="yuyongpeng@hotmail.com",
    description=("专门用于处理队列的上链操作"),
    # long_description=README + '\n\n' + CHANGES,
    # long_description_content_type="text/markdown",
    # long_description_markdown_filename='README.md',
    # license="MIT",
    # long_description= read('README.md'),
    license=open('LICENSE').read(),
    keywords="solidity web3 constract sdk",
    url="https://gitlab.hard-chain.cn/cport/upload_chain",
    # packages=['upload_chain'],  # 需要打包的目录列表
    packages=find_packages(where='.', exclude=('tests', 'tests.*'), include=('*',)),
    # 需要安装的依赖
    install_requires=[
        'pycontractsdk',    # 对web3的封装
        'sierra-utils-rand',
        'clock',
        'peewee==3.9.3',
        'arrow==0.13.1',
        'pymysql==0.9.3',
        'celery==4.3.0',
        'pika==1.0.0',
        'kafka==1.3.5',
        'retry==0.9.2',
        'redis==3.2.1',
        'requests==2.21.0',
        #logzero
        'logbook==1.4.3',
        'toolz==0.9.0',
        'wrapt==1.11.1',
        'click==7.0',
        'random2',
        'python-common-cache==0.1',
        'wechatpy[cryptography]==1.8.1',
        'cryptography==2.6.1',
        'rsa==4.0',
    ],
    py_modules=['upload_chain'],
    python_requires='>=3.6',
    setup_requires=['setuptools-markdown'],
    # 添加这个选项，在windows下Python目录的scripts下生成exe文件
    # 注意：模块与函数之间是冒号:
    entry_points={'console_scripts': [
        'uploadchain_service = upload_chain.main:upload_chain',                          # 上链的消费者程序
        'uploadchain_service_army = upload_chain.main:upload_chain_army',                # ARMY上链的消费者程序
        'validation_service = upload_chain.main:validation_chain',                       # 单进程方式验证数据是否已经上链
        'validation_multiproc_service = upload_chain.main:validation_chain_multi_proc',  # 多进程方式验证数据是否已经上链
    ]},
    # 会把这个list中的文件copy到系统的PATH路径下
    scripts=['run.sh'],
    classifiers=[  # 程序的所属分类列表
        "Development Status :: 3 - Alpha",
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Topic :: Utilities",
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
    ],
    zip_safe=False
)
