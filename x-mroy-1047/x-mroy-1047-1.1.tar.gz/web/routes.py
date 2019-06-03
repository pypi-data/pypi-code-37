import os
import random
import json
import  asyncio
from ashares.remote import  AsyncConnection
from enuma_elish.book import  Book
import  logging


def select_routes(geo=None,number=3, entry=None, out=None, exclude=None, ss_dir="/tmp/ss-random"):
    confs  = []
    for f in os.listdir(ss_dir):
        with open(os.path.join(ss_dir, f)) as fp:
            confs.append(json.load(fp))
    random.shuffle(confs)
    def whereis(conf,exclude=None,include=None, n=3):
        if not geo:
            return 'Unknow'
        ip = conf.get("server")
        name = geo.city(ip).city.name
        name = name if name else "Unknow"
        return name.lower()
    code = 0
    if not entry:
        code ^= 1
    if not out:
        code ^= 2
    bak = []
    b = []
    for c in confs:
        city = whereis(c)
        if entry and not isinstance(entry,dict) and  entry in city:
            # print("found", c, city)
            entry = c
        
        if out and not isinstance(out,dict) and out in city:
            # print("found", c)
            out = c

        if exclude and exclude in city:
            continue

        bak.append(c)
    if not isinstance(entry, dict):
        code ^= 1
        entry = random.choice(bak)
        bak.remove(entry)

    if not isinstance(out, dict):
        code ^= 2
        out = random.choice(bak)
        bak.remove(out)
        
    if number  < 3:
        return [entry, out]

    for i in range(number -2):
        o = random.choice(bak)
        bak.remove(o)
        b.append(o)
    return code, [entry] + b + [out]


async def ensure_func(host, ss_dir):
    ip = host.host
    port = int(host.port)
    pwd = host.passwd
    conf_path = os.path.join(ss_dir, ip)
    if not os.path.exists(conf_path):
        a = AsyncConnection(host=ip, name='root', port=port, password=pwd, keyfile=None)
        a.timeout_t = 12
        _,_,t, _ = await a.tcp_ping(port)
        if t < 999:
            res = await a.enuma_elish()
            if len(res) > 1 and res[-1] == 0:
                return True
            else:
                logging.error(str(res))
        else:
            logging.error("22 port is not connected")
        
        return  False
    else:
        return  True

async def _init_routes(db, Obj, ss_dir):
    try:
        hosts = [i for i in db.query(Obj)]
        s = [ensure_func(host, ss_dir) for host in hosts]
        return  await asyncio.gather(*s)
    except  Exception as e:
        raise  e

def init_routes(db, Obj, ss_dir):
    loop = asyncio.new_event_loop()
    # ips = [i['server'] for i in confs]
    uset = loop.run_until_complete(_init_routes(db, Obj, ss_dir))

def build_routes(confs):
    for i in range(len(confs)):
        confs[i]['server_port'] = int(confs[i]['server_port'])
    # print(confs)
    return Book.Links(confs)
    
    
