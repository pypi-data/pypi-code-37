import requests
import json


class IPInfo:

    def __init__(self, ip=""):
        url = "https://ipinfo.io/json"
        if not(ip == ""):
            url = "https://ipinfo.io/" + ip + "/json"
        j = requests.get(url).content.decode()
        j = json.loads(j)
        self.ip = j['ip']
        self.hostname = j['hostname']
        self.city = j['city']
        self.region = j['region']
        self.country = j['country']
        self.coordinates = j['loc']
        coords = self.coordinates.split(',')
        self.lat = coords[0]
        self.long = coords[1]
        self.org = j['org']