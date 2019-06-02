import datetime
import pytz

from django.conf import settings
from django.utils.timezone import now


def get_coverpage_conf():
    config = getattr(settings, 'WEBSITE_COVERPAGE', {})
    return (
        config,
        config.get('active', True),
        config.get('url', '/coverpage/'),
        config.get('cookiename', 'coverpage')
    )

def coverpage_is_available(request):
    config, active, url, cookiename = get_coverpage_conf()

    # bail out if obviously not active
    if not active:
        return False

    # check files to ignore
    ignore_files = config.get('ignore_files', [
        '/favicon.ico',
        '/robots.txt'
    ])
    for ig in ignore_files:
        if request.path.startswith(ig):
            return False

    # check urls to ignore
    ignore_urls = config.get('ignore_urls', [])
    for ig in ignore_urls:
        if request.path.startswith(ig):
            return False


    # ignore common bots
    ua = request.META.get('HTTP_USER_AGENT', '').lower()
    bots = [
        '360spider',
        'adsbot-google',
        'ahrefs',
        'apachebench', # not a bot, but it can go here
        'archive.org',
        'baiduspider',
        'bingbot',
        'bingpreview',
        'dotbot',
        'duckduckgo',
        'duckduckbot',
        'exabot',
        'facebook',
        'feedfetcher-google',
        'googlebot',
        'googleimageproxy',
        'ia_archiver',
        'mediapartners-google',
        'mj12bot',
        'msnbot',
        'panscient.com',
        'pinterest',
        'slackbot',
        'slurp',
        'sogou',
        'surveybot',
        'twitterbot',
        'voilabot',
        'yahoo-mmcrawler',
        'yahoomailproxy',
        'yandexbot'
    ]
    for bot in bots:
        if bot in ua:
            return False

    # check start time
    dt_from = config.get('start', None)
    if dt_from is not None:
        tz = pytz.timezone(settings.TIME_ZONE) if settings.USE_TZ else None
        dt_from = datetime.datetime(*dt_from, tzinfo=tz)
        if now() < dt_from:
            return False

    # check end time
    dt_to = config.get('end', None)
    if dt_to is not None:
        tz = pytz.timezone(settings.TIME_ZONE) if settings.USE_TZ else None
        dt_to = datetime.datetime(*dt_to, tzinfo=tz)
        if now() > dt_to:
            return False

    # coverpage is available to be viewed
    return True
