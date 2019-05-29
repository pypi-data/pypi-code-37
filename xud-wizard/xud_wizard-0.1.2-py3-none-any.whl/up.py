import threading
import os
from .utils import get_service
import pexpect
import logging
import urllib.request
from .down import main as down
from .shell import main as shell
import subprocess

btc_ok = False
ltc_ok = False
eth_ok = False

btc_stop_event = threading.Event()
ltc_stop_event = threading.Event()
eth_stop_event = threading.Event()


def expect(cmd):
    return pexpect.spawn(cmd)


def wait_bitcoind_synced():
    bitcoind = get_service('bitcoind')
    status = bitcoind.status
    while status != "OK":
        print('[bitcoind] ' + status)
        btc_stop_event.wait(30)
        if btc_stop_event.is_set():
            raise Exception("bitcoind waiting interrupted")
        status = bitcoind.status


def wait_litecoind_synced():
    litecoind = get_service('litecoind')
    status = litecoind.status
    while status != "OK":
        print('[litecoind] ' + status)
        ltc_stop_event.wait(30)
        if ltc_stop_event.is_set():
            raise Exception("litecoind waiting interrupted")
        status = litecoind.status


def wait_geth_synced():
    geth = get_service('geth')
    status = geth.status
    while status != "OK":
        print('[geth] ' + status)
        eth_stop_event.wait(30)
        if eth_stop_event.is_set():
            raise Exception("geth waiting interrupted")
        status = geth.status


def docker_compose_up(service):
    p = subprocess.Popen('docker-compose up -d ' + service, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    stdout, stderr = p.communicate()
    r = p.returncode
    if r != 0:
        logging.error("Failed to start up service: %s", service)
        exit(1)


def create_lnd_wallet(network, chain, password):
    service = None
    if chain == 'bitcoin':
        service = 'lndbtc'
    elif chain == 'litecoin':
        service = 'lndltc'
    child = expect("docker-compose exec {} lncli -n {} -c {} create".format(service, network, chain))
    child.expect('Input wallet password: ')
    child.sendline(password)
    child.expect('Confirm wallet password: ')
    child.sendline(password)
    # Do you have an existing cipher seed mnemonic you want to use? (Enter y/n):
    child.expect("Do you have an existing cipher seed mnemonic you want to use")
    child.sendline("n")
    # Input your passphrase if you wish to encrypt it (or press enter to proceed without a cipher seed passphrase):
    child.expect("Input your passphrase if you wish to encrypt it")
    child.sendline()
    # Generating fresh cipher seed...
    #
    # !!!YOU MUST WRITE DOWN THIS SEED TO BE ABLE TO RESTORE THE WALLET!!!
    #
    # ---------------BEGIN LND CIPHER SEED---------------
    #  1. abandon   2. ride      3. shine     4. return
    #  5. twelve    6. receive   7. promote   8. hood
    #  9. nut      10. upset    11. pave     12. tag
    # 13. note     14. glory    15. violin   16. borrow
    # 17. slush    18. square   19. country  20. outdoor
    # 21. garment  22. clutch   23. grocery  24. rotate
    # ---------------END LND CIPHER SEED-----------------
    #
    # !!!YOU MUST WRITE DOWN THIS SEED TO BE ABLE TO RESTORE THE WALLET!!!
    #
    # lnd successfully initialized!
    child.expect("lnd successfully initialized")

    if child.isalive():
        child.close()


def unlock_lnd_wallet(network, chain, password):
    service = None
    if chain == 'bitcoin':
        service = 'lndbtc'
    elif chain == 'litecoin':
        service = 'lndltc'
    child = expect("docker-compose exec {} lncli -n {} -c {} unlock".format(service, network, chain))
    child.expect('Input wallet password: ')
    child.sendline(password)
    # lnd successfully unlocked!
    # unlock.expect('lnd successfully unlocked')
    # [lncli] rpc error: code = Unknown desc = wallet not found
    child.expect(".*")
    print(child.before)

    if child.isalive():
        child.close()


def up_btc(network):
    global btc_ok
    try:
        docker_compose_up("bitcoind")
        wait_bitcoind_synced()
        docker_compose_up("lndbtc")

        log = expect('docker-compose logs -f lndbtc')
        # [INF] LTND: Waiting for wallet encryption password. Use `lncli create` to create a wallet, `lncli unlock` to unlock an existing wallet, or `lncli changepassword` to change the password of an existing wallet and unlock it.
        log.expect('Waiting for wallet encryption password')

        password_path = "data/lndbtc/password.txt"

        if not os.path.exists(password_path):
            password = '12345678'
            with open(password_path) as f:
                f.write(password)
            create_lnd_wallet(network, "bitcoin", password)

        password = open(password_path).read()

        # unlock wallets
        unlock_lnd_wallet(network, "bitcoin", password)

        # validate lndbtc started
        # [INF] RPCS: RPC server listening on 0.0.0.0:10009
        log.expect('RPC server listening on')

        if log.isalive():
            log.close()

        btc_ok = True
    except:
        logging.exception("Failed to start up btc")
        exit(1)


def up_ltc(network):
    global ltc_ok
    try:
        ltc_stop_event.wait(2)
        docker_compose_up("litecoind")
        wait_litecoind_synced()
        docker_compose_up("lndltc")

        log = expect('docker-compose logs -f lndltc')
        # [INF] LTND: Waiting for wallet encryption password. Use `lncli create` to create a wallet, `lncli unlock` to unlock an existing wallet, or `lncli changepassword` to change the password of an existing wallet and unlock it.
        log.expect('Waiting for wallet encryption password')

        password_path = "data/lndltc/password.txt"

        if not os.path.exists(password_path):
            password = '12345678'
            with open(password_path) as f:
                f.write(password)
            create_lnd_wallet(network, "litecoin", password)

        password = open(password_path).read()

        # unlock wallets
        unlock_lnd_wallet(network, "litecoin", password)

        # validate lndbtc started
        # [INF] RPCS: RPC server listening on 0.0.0.0:10009
        log.expect('RPC server listening on')

        if log.isalive():
            log.close()

        ltc_ok = True
    except:
        logging.exception("Failed to start up ltc")
        exit(1)


def up_eth(network):
    global eth_ok
    try:
        eth_stop_event.wait(4)
        docker_compose_up("geth")
        wait_geth_synced()
        docker_compose_up("raiden")
        eth_ok = True
    except:
        logging.exception("Failed to up eth")
        exit(1)


def up_xud(network):
    try:
        docker_compose_up("xud")
    except:
        logging.exception("Failed to start up xud")
        exit(1)


def download_docker_compose_yaml_file(network):
    # download docker-compose.yml
    url = "https://raw.githubusercontent.com/ExchangeUnion/xud-docker/master/xud-{}/docker-compose.yml".format(network)
    urllib.request.urlretrieve(url, 'docker-compose.yml')
    logging.info("Downloaded docker-compose.yml")


def init(network):
    t1 = threading.Thread(target=up_btc, args=(network,))
    t2 = threading.Thread(target=up_ltc, args=(network,))
    t3 = threading.Thread(target=up_eth, args=(network,))

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

    if btc_ok and ltc_ok and eth_ok:
        up_xud(network)
    else:
        raise Exception("Failed to init")


def main(network):
    try:
        down(network)
        download_docker_compose_yaml_file(network)
        init(network)
        shell(network)
    except KeyboardInterrupt:
        btc_stop_event.set()
        ltc_stop_event.set()
        eth_stop_event.set()




