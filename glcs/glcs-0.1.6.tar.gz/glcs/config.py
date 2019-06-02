import json
from xdg import (XDG_CONFIG_DIRS, XDG_CONFIG_HOME,
                 XDG_DATA_HOME, XDG_DATA_DIRS)
from pathlib import Path


def update_db_settings(engine, name, user, passw, host, port):
    cfgdata = {}
    cfgdata['engine'] = engine
    if cfgdata["engine"] == "mysql":
        cfgdata["engine"] = "django.db.backends.mysql"
    cfgdata['name'] = name
    cfgdata['user'] = user
    cfgdata['password'] = passw
    cfgdata['host'] = host
    cfgdata['port'] = port
    if not Path(XDG_CONFIG_HOME).exists():
        print(str(XDG_CONFIG_HOME) + " does not exist, creating...")
        Path(XDG_CONFIG_HOME).mkdir()
    cfgpath = Path(XDG_CONFIG_HOME) / "glcs"
    if not Path(cfgpath).exists():
        print(str(cfgpath) + " does not exist, creating...")
        Path(cfgpath).mkdir()
    cfgloc = cfgpath / "database.cfg"
    if not Path(cfgloc).exists():
        print(str(cfgloc) + " does not exist, creating...")
        for setting in cfgdata:
            if cfgdata[setting] is None:
                print("Value unset for database " + str(setting))
                print("Initial creation requires all values be set.")
                print("Aborting")
                return
        with open(cfgloc, "w+") as cfgfile:
            json.dump(cfgdata, cfgfile, indent=2)
    else:
        print("Existing database config found, updating")
        oldcfg = dict()
        with open(cfgloc, "r") as cfgfile:
            oldcfg = json.load(cfgfile)
        for setting in cfgdata:
            if cfgdata[setting] is not None:
                oldcfg[setting] = cfgdata[setting]
        with open(cfgloc, "w+") as cfgfile:
            json.dump(oldcfg, cfgfile, indent=2)


def load_db_settings():
    cfgloc = Path(XDG_CONFIG_HOME) / "database.cfg"
    cfgdata = dict()
    if not Path(cfgloc).exists():
        print(str(cfgloc) + " not found, aborting.")
        return None
    with open(cfgloc, "r") as cfgfile:
        cfgdata = json.load(cfgfile)
    return cfgdata
