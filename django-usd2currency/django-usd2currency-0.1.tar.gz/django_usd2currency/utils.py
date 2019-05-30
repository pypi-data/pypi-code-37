import requests
from django.conf import settings
from django.core.cache import cache


DEFAULT_CURRENCIES = ['CNY', 'EUR', 'JPY', 'KRW']
APILAYER_ACCESS_KEY = getattr(settings, 'APILAYER_ACCESS_KEY', None)
APILAYER_CURRENCIES = getattr(settings,
                              'APILAYER_CURRENCIES',
                              DEFAULT_CURRENCIES)


if APILAYER_ACCESS_KEY is None:
    raise Exception("Need set APILAYER_ACCESS_KEY in settings.py !")


if getattr(cache, 'lock', None):
    Lock = lambda: cache.lock('lock_update_rate')
else:
    from threading import Lock


def get_symbol(currency):
    return 'USD%s' % currency.upper()


def update_rate(currency):
    resp = requests.get(
        'http://apilayer.net/api/live?access_key=%s&format=1&currencies=%s' % (
            APILAYER_ACCESS_KEY,
            ','.join(APILAYER_CURRENCIES)))

    d = resp.json()
    for symbol in d['quotes']:
        rate = d['quotes'][symbol]
        cache.set(symbol, rate, 86400)  # 1 day expire

    return d['quotes'][get_symbol(currency)]


def get_rate_from_usd(currency):
    v = cache.get(get_symbol(currency))
    if v:
        return v
    # Ensure update rate call only once as of api ratelimit
    with Lock():
        v = cache.get(get_symbol(currency))
        if v:
            return v
        return update_rate(currency)


def usd2currency(v, currency='CNY'):

    if currency.upper() == 'USD':
        return v
    rate = get_rate_from_usd(currency)
    return round(rate * v, 2)
