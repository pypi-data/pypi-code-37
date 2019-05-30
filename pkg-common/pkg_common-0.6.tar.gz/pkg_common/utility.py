import os
from decimal import Decimal

from cryptography.fernet import Fernet


KEY = b'WV9PaFYoxFoURR9ABpNTxRjuxAtJRx2j1zg_wNqaENY='


def encrypt(info):
    f = Fernet(os.environ.get('KEY_SECRET', KEY))
    return f.encrypt(info.encode())


def decrypt(info):
    f = Fernet(os.environ.get('KEY_SECRET', KEY))
    return f.decrypt(info).decode()


def to_decimal(text):
    cleanedvalue = ''.join([i for i in text if i.isdigit()])
    if len(cleanedvalue) == 0:
        return 0
    return Decimal(text.replace('R$', '').replace('*', '').replace('.', '').replace(',', '.'))