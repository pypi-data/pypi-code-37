from babel import dates
from datetime import date
from functools import partial

from pyramid.events import subscriber
from pyramid.events import BeforeRender

from .models import load_yaml


@subscriber(BeforeRender)
def add_global(event):
    event['globals'] = {
        'format_date':
        partial(dates.format_date, locale=event['request'].locale_name),
        'format_datetime':
        partial(dates.format_datetime, locale=event['request'].locale_name),
        'today':
        date.today(),
    }


@subscriber(BeforeRender)
def add_data(event):
    try:
        event['data'] = load_yaml('globals.yaml', True)
    except FileNotFoundError:
        event['data'] = {}


@subscriber(BeforeRender)
def add_menu(event):
    try:
        event['menu'] = load_yaml('menu/default.yaml', True)
    except FileNotFoundError:
        event['menu'] = []
