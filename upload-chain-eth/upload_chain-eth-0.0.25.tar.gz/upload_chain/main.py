#!/usr/bin/env python
# -*- coding=UTF-8 -*-

from upload_chain import setting
import click
from upload_chain import cusomer
from upload_chain.setting import VAR
from pycontractsdk.contracts import Contract
from upload_chain.utils import import_plugins


@click.command()
@click.option('-f', "--file", default='/etc/upload_chain.conf', help='指定配置文件的路径（默认: /etc/upload_chain.conf）')
def upload_chain_army(file):
    """
    消费队列中的数据，进行上链操作
    :param file:
    :return:
    """
    import_plugins()
    # 初始化配置信息
    setting.read_config_army(file)
    # 实例化 Contract
    provider = VAR['ETH_PROVIDER']
    contract_address = VAR['CONTRACT_ADDRESS']
    abi = VAR['CONTRACT_ABI']
    operator_private_key = VAR['OPERATOR_PRIVATEKEY']
    delegate_private_key = VAR['DELEGATE_PRIVATEKEY']
    gas = VAR['GAS']
    gas_prise = VAR['GAS_PRISE']
    concart = Contract(provider=provider, timeout=60, contract_address=contract_address, abi=abi,
                  private_key=operator_private_key,
                  gas=int(gas),
                  gas_prise=int(gas_prise)
                  )
    # 启动 消费者程序
    cus = cusomer.CallContract(
        contracrt=concart,
        queue_name=VAR['QUEUE_NAME'],
        queue_ip=VAR['QUEUE_IP'],
        queue_port=VAR['QUEUE_PORT'],
        queue_user=VAR['QUEUE_USER'],
        queue_password=VAR['QUEUE_PASSWORD'],
        queue_vhost=VAR['QUEUE_VHOST'],
    )
    cus.cusomer()
    # from concurrent.futures import ProcessPoolExecutor
    # with ProcessPoolExecutor(max_workers=5) as executor:
    #     executor.submit(cus.cusomer)
    #     executor.submit(cus.cusomer)
    #     executor.submit(cus.cusomer)
    #     executor.submit(cus.cusomer)
    #     executor.submit(cus.cusomer)


@click.command()
@click.option('-f', "--file", default='/etc/upload_chain.conf', help='指定配置文件的路径（默认: /etc/upload_chain.conf）')
def upload_chain(file):
    """
    消费队列中的数据，进行上链操作
    :param file:
    :return:
    """
    import_plugins()
    # 初始化配置信息
    setting.read_config2(file)
    # 实例化 Contract
    provider = VAR['ETH_PROVIDER']
    contract_address = VAR['CONTRACT_ADDRESS']
    abi = VAR['CONTRACT_ABI']
    operator_private_key = VAR['OPERATOR_PRIVATEKEY']
    delegate_private_key = VAR['DELEGATE_PRIVATEKEY']
    gas = VAR['GAS']
    gas_prise = VAR['GAS_PRISE']
    concart = Contract(provider=provider, timeout=60, contract_address=contract_address, abi=abi,
                  private_key=operator_private_key,
                  gas=int(gas),
                  gas_prise=int(gas_prise)
                  )
    # 启动 消费者程序
    cus = cusomer.CallContract(
        contracrt=concart,
        queue_name=VAR['QUEUE_NAME'],
        queue_ip=VAR['QUEUE_IP'],
        queue_port=VAR['QUEUE_PORT'],
        queue_user=VAR['QUEUE_USER'],
        queue_password=VAR['QUEUE_PASSWORD'],
        queue_vhost=VAR['QUEUE_VHOST'],
    )
    cus.cusomer()
    # from concurrent.futures import ProcessPoolExecutor
    # with ProcessPoolExecutor(max_workers=5) as executor:
    #     executor.submit(cus.cusomer)
    #     executor.submit(cus.cusomer)
    #     executor.submit(cus.cusomer)
    #     executor.submit(cus.cusomer)
    #     executor.submit(cus.cusomer)


@click.command()
@click.option('-f', "--file", default='/etc/upload_chain.conf', help='指定配置文件的路径（默认: /etc/upload_chain.conf）')
def validation_chain(file):
    """ 用于验证数据是否上链 """
    import_plugins()
    # 初始化配置信息
    setting.read_config2(file)

    # 实例化 Contract
    provider = VAR['ETH_PROVIDER']
    contract_address = VAR['CONTRACT_ADDRESS']
    abi = VAR['CONTRACT_ABI']
    operator_private_key = VAR['OPERATOR_PRIVATEKEY']
    delegate_private_key = VAR['DELEGATE_PRIVATEKEY']
    gas = VAR['GAS']
    gas_prise = VAR['GAS_PRISE']
    concart = Contract(provider=provider, timeout=60, contract_address=contract_address, abi=abi,
                       private_key=operator_private_key,
                       gas=gas,
                       gas_prise=gas_prise
                       )
    # 启动 消费者程序
    cus = cusomer.ValidationContract(
        contracrt=concart,
        queue_name=VAR['QUEUE_NAME_VALIDATION'],
        queue_ip=VAR['QUEUE_IP'],
        queue_port=VAR['QUEUE_PORT'],
        queue_user=VAR['QUEUE_USER'],
        queue_password=VAR['QUEUE_PASSWORD'],
        queue_vhost=VAR['QUEUE_VHOST'],
    )
    cus.cusomer()
    # from concurrent.futures import ProcessPoolExecutor
    # with ProcessPoolExecutor(max_workers=5) as executor:
    #     executor.submit(cus.cusomer)
    #     executor.submit(cus.cusomer)
    #     executor.submit(cus.cusomer)
    #     executor.submit(cus.cusomer)
    #     executor.submit(cus.cusomer)


@click.command()
@click.option('-f', "--file", default='/etc/upload_chain.conf', help='指定配置文件的路径（默认: /etc/upload_chain.conf）')
def validation_chain_multi_proc(file):
    """ 多进程的方式来运行验证程序 """
    import_plugins()
    # 初始化配置信息
    setting.read_config2(file)
    from upload_chain.cusomer import ValidationChainWorker
    from multiprocessing import cpu_count
    jobs = []
    for i in range(cpu_count()):
        p = ValidationChainWorker(i)
        jobs.append(p)
        p.start()
        print("count : {}".format(len(jobs)))
    for j in jobs:
        j.join()
    print("count22 : {}".format(len(jobs)))


if __name__ == "__main__":
    upload_chain()
    # validation_chain_multi_proc()
