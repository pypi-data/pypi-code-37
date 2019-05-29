# -*- coding: utf-8 -*-
from django.conf import settings as dj_settings
from appconf import AppConf
from decimal import Decimal
from django.utils.translation import ugettext_lazy as _

settings = dj_settings

class PayuAppConf(AppConf):

    PAYU_API_ORDER_MODEL = 'module.Model'
    PAYU_API_PAYMENT_MODEL = None
    PAYU_API_TESTING = True
    PAYU_API_NOTIFY_URL = None
    PAYU_API_CLIENT_SECRET = None
    PAYU_API_POS_ID = None
    PAYU_API_SECOND_KEY = None

    CURRENCY = 'PLN'

    if hasattr(settings, 'PAYU_API_TESTING'):
        TESTING = settings.PAYU_API_TESTING
    else:
        TESTING = False

    if TESTING:
        NOTIFY_URL = 'http://snd.integree.eu/notify'
        AUTH_URL = 'https://secure.snd.payu.com/pl/standard/user/oauth/authorize'
        ORDER_URL = 'https://secure.snd.payu.com/api/v2_1/orders/'
        DELETE_TOKEN_URL = 'https://secure.snd.payu.com/api/v2_1/tokens/'
        PAYMETHODS_URL = 'https://secure.snd.payu.com/api/v2_1/paymethods/'
    else:
        NOTIFY_URL = 'http://snd.integree.eu/notify'
        AUTH_URL = 'https://secure.payu.com/pl/standard/user/oauth/authorize'
        ORDER_URL = 'https://secure.payu.com/api/v2_1/orders/'
        DELETE_TOKEN_URL = 'https://secure.payu.com/api/v2_1/tokens/'
        PAYMETHODS_URL = 'https://secure.payu.com/api/v2_1/paymethods/'

    PAYMENT_MODEL = None

    PLN = 'PLN'
    EUR = 'EUR'
    USD = 'USD'
    CZK = 'CZK'
    GBP = 'GBP'

    CURRENCY_CHOICE = (
        (PLN, u"Złoty"),
        (EUR, u"Euro"),
        (USD, u"Dolar amerykański"),
        (CZK, u"Korona czeska"),
        (GBP, u"Funt brytyjski"),
    )

    CURRENCY_DATA = {
        PLN: {
          'name': u"Złoty",
          'sub_unit': Decimal(100),
        },
        EUR: {
          'name': u"Euro",
          'sub_unit': Decimal(100),
        },
        USD: {
          'name': u"Dolar amerykański",
          'sub_unit': Decimal(100),
        },
        CZK: {
          'name': u"Korona czeska",
          'sub_unit': Decimal(100),
        },
        GBP: {
          'name': u"Funt brytyjski",
          'sub_unit': Decimal(100),
        },
    }
