import re
import os
from django.urls import get_resolver
from django.utils.module_loading import import_string

from .settings import FALLBACK_VIEW


def get_fallback_view():
    return import_string(FALLBACK_VIEW)


def get_unique_urls(resolver=None, prefix=""):
    if resolver is None:
        resolver = get_resolver()
    all_urls = []
    for k,v in resolver.reverse_dict.items():
        full = "{}/{}".format(prefix, v[0][0][0])
        full = os.path.normpath(full)
        all_urls.append(full)
    for k,v in resolver.namespace_dict.items():
        all_urls.extend(get_unique_urls(v[1], "{}/{}".format(prefix, v[0])))
    all_urls = set(all_urls)
    return all_urls


def get_excluding_regex(unique_urls=None):
    if unique_urls is None:
        unique_urls = get_unique_urls()
    exclude_group = r"(?!^/{}/?$)"
    excluded = []
    for unique_url in unique_urls:
        unique_url = re.sub(r"\%\(.+\)s", "[\\\w\\\d-]+", unique_url)
        unique_url = os.path.normpath(unique_url)
        if unique_url.startswith("/"):
            unique_url = unique_url[1:]
        if unique_url.endswith("/"):
            unique_url = unique_url[:-1]
        if unique_url == ".":
            unique_url = ""
        excluded.append(exclude_group.format(unique_url))
    joined = "".join(excluded)
    regex = r"{excluded}.+/?$".format(excluded=joined)
    return regex


