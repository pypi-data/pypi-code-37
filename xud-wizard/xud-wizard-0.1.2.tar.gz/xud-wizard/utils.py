import platform
import os
from .rpc.bitcoind import Bitcoind
from .rpc.lnd import Lnd
from .rpc.raiden import Raiden
from .rpc.xud import Xud
from .rpc.geth import Geth
from fabric import Connection
import logging
import base64

# Hide CryptographyDeprecationWarning: encode_point has been deprecated on EllipticCurvePublicNumbers and will be removed in a future version. Please use EllipticCurvePublicKey.public_bytes to obtain both compressed and uncompressed point encoding.
#   m.add_string(self.Q_C.public_numbers().encode_point())
# Ref. https://stackoverflow.com/a/55336269/2663029
import warnings
warnings.filterwarnings(action='ignore',module='.*paramiko.*')

prefix = "XUD_DOCKER_"

HOME = prefix + "HOME"
HOST = prefix + "HOST"

services = {}


def print_services(title, services):
    c1w = max(len(title[0]), len(max(services.keys(), key=len)))
    c2w = max(len(title[1]), len(max(services.values(), key=len)))
    c1f = '{:' + str(c1w) + "}"
    c2f = '{:' + str(c2w) + "}"

    print(("┏━━" + c1f + "━━┯━━" + c2f + "━━┓").format("━" * c1w, "━" * c2w))
    print(("┃  " + c1f + "  │  " + c2f + "  ┃").format(title[0], title[1]))

    for key, value in services.items():
        print(("┠──" + c1f + "──┼──" + c2f + "──┨").format("─" * c1w, "─" * c2w))
        print(("┃  " + c1f + "  │  " + c2f + "  ┃").format(key, value))

    print(("┗━━" + c1f + "━━┷━━" + c2f + "━━┛").format("━" * c1w, "━" * c2w))


def get_home():
    """
    :return:
    Linux
        /home/<user>/.xud-docker
    Darwin (macOS)
        /Users/<user>/Library/Application Support/XudDocker
    Windows
        C:\\Users\\<user>\\AppData\\Local\\XudDocker
    """
    if HOME in os.environ:
        return os.environ[HOME]

    if platform.system() == 'Linux':
        return os.path.expanduser("~/.xud-docker")
    elif platform.system() == 'Darwin':
        return os.path.expanduser("~/Library/Application Support/XudDocker")
    elif platform.system() == 'Windows':
        return os.path.expanduser("~/AppData/Local/XudDocker")


def get_connection(host):
    c = Connection('yy@' + host)
    return c


def load_content(host, path):
    if is_local():
        return open(path, 'rb').read()
    else:
        if "macaroon" in path:
            result = get_connection(host).run('cat ' + path + " | base64", hide=True).stdout
            return base64.b64decode(result)
        else:
            result = get_connection(host).run('cat ' + path, hide=True).stdout
            return result.encode()


def build_service(name):
    host = get_host()
    data = get_home() + '/data'

    if name == 'bitcoind':
        connstr_bitcoind = "http://xu:xu@{}:18332".format('localhost')
        s = Bitcoind(connstr_bitcoind)
    elif name == 'litecoind':
        connstr_litecoind = "http://xu:xu@{}:19332".format('localhost')
        s = Bitcoind(connstr_litecoind)
    elif name == 'lndbtc':
        connstr_lndbtc = "{}:10009".format('localhost')
        path_lndbtc_macaroon = data + '/lndbtc/data/chain/bitcoin/testnet/admin.macaroon'
        path_lndbtc_cert = data + '/lndbtc/tls.cert'
        lndbtc_macaroon = load_content(host, path_lndbtc_macaroon)
        lndbtc_cert = load_content(host, path_lndbtc_cert)
        s = Lnd(connstr_lndbtc, lndbtc_cert, lndbtc_macaroon)
    elif name == 'lndltc':
        connstr_lndltc = "{}:20009".format('localhost')
        path_lndltc_macaroon = data + '/lndltc/data/chain/litecoin/testnet/admin.macaroon'
        path_lndltc_cert = data + '/lndltc/tls.cert'
        lndltc_macaroon = load_content(host, path_lndltc_macaroon)
        lndltc_cert = load_content(host, path_lndltc_cert)
        s = Lnd(connstr_lndltc, lndltc_cert, lndltc_macaroon)
    elif name == 'geth':
        connstr_geth = "http://{}:8545".format('localhost')
        s = Geth(connstr_geth)
    elif name == 'raiden':
        connstr_raiden = "http://{}:5000".format('localhost')
        s = Raiden(connstr_raiden)
    elif name == 'xud':
        connstr_xud = "{}:8886".format('localhost')
        path_xud_cert = data + '/xud/tls.cert'
        xud_cert = load_content(host, path_xud_cert)
        s = Xud(connstr_xud, xud_cert)
    else:
        raise Exception('Unsupported service name: ' + name)

    return s


def get_service(name):
    if name in services:
        return services[name]

    s = build_service(name)
    services[name] = s

    return s


def get_host():
    """
    :return: localhost
    """
    if HOST in os.environ:
        return os.environ[HOST]

    return "localhost"


def is_local():
    return get_host() == 'localhost'

