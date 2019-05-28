import os

from .etna import EtnaWrapper

import logging

logging.basicConfig(level=logging.DEBUG)


def _load_config():
    return {'login': 'massar_t', 'password': os.environ.get('ETNA_PASS')}


def main():
    creds = _load_config()
    e = EtnaWrapper(**creds)
    print(e.get_user_info())


main()
