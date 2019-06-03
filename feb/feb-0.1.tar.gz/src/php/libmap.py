import json

import requests

from util.output import Output
from util.urlhelper import URLHelper


class LibMap(object):
    _name2uri = {}
    _uri2name = {}
    _config = {}
    _init = False
    URL_LIBMAP = "https://git.xiaojukeji.com/fangjunda/cc/blob/master/feb/libmap.json"
    URL_LIBMAP_RAW = "https://git.xiaojukeji.com/fangjunda/cc/raw/master/feb/libmap.json"

    @staticmethod
    def init():
        r = requests.get(LibMap.URL_LIBMAP_RAW)
        if not r.ok:
            Output.error("Fetch config from git failed {url}".format(url=LibMap.URL_LIBMAP_RAW))
            return

        LibMap._config = r.json()

        for name, uri in LibMap._config.items():
            LibMap._name2uri[name] = uri
            LibMap._uri2name[uri] = name

        LibMap._init = True

    @staticmethod
    def get_uri(name, default=None):
        if not LibMap._init:
            LibMap.init()
        return LibMap._name2uri.get(name, default)

    @staticmethod
    def get_name(url, default=None):
        if not LibMap._init:
            LibMap.init()
        return LibMap._uri2name.get(URLHelper.get_uri(url), default)


class Data(object):
    url = ""
    name = ""
    type = "git"
    branch = ""
    as_version = "master"
    dev = False

    def short(self):
        return "{name:<{max_len}} - {url}".format(name=self.name, max_len=DataStore.max_key_len, url=self.url)

    def detail(self):
        return """======== {name} ========
        name:   {name}
        branch: {branch}
        as_ver: {as_version}
        is_dev: {dev}
        type:   {type}
        url:    {url}
        """.format(
            name=self.name, branch=self.branch, as_version=self.as_version, dev=self.dev,
            type=self.type, url=self.url
        )


class DataStore(object):
    store = {}
    max_key_len = 0

    @staticmethod
    def set(key, value):
        if key in DataStore.store:
            data = DataStore.store[key]
        else:
            data = Data()
            data.name = key
            if DataStore.max_key_len < len(key):
                DataStore.max_key_len = len(key)

            Output.debug("New key {key}".format(key=key))

        if "url" in value:
            data.url = value["url"]
        if "type" in value:
            data.type = value["type"]
        if "branch" in value:
            data.branch = value["branch"]
        if "as_version" in value:
            data.as_version = value["as_version"]
        if "dev" in value:
            data.dev = value["dev"]

        DataStore.store[key] = data

    @staticmethod
    def get(key):
        return DataStore.store.get(key, None)
