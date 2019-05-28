import requests
import json

class Goodwe(object):
    """ 
    Class represents the Goodwe Invertor
    """

    def __init__(self, usr, pwd, system_id):

        self._session = requests.Session()
        self._system_id = system_id
        self._usr = usr
        self._pwd = pwd
        self._token =  '{"version":"v2.0.4","client":"ios","language":"en"}'
        self.prefix = 'https://euapi.sems.com.cn/api/v1/'
        self.inverterData = None
        self.login()
        self.get_current_reading()

    def _post(self, url, headers, payload):
        return self._session.request('POST', url, headers=headers, data=payload)

    def login(self):
        headers = { 'User-Agent': 'PVMaster/2.0.4 (iPhone; iOS 11.4.1; Scale/2.00)', 'Token': self._token }
        loginPayload = {'account': self._usr, 'pwd': self._pwd }
        r = self._post(self.prefix + 'Common/CrossLogin', headers= headers, payload=loginPayload)
        self._token = json.dumps(r.json()['data'])

    def get_current_reading(self):
        headers = { 'User-Agent': 'PVMaster/2.0.4 (iPhone; iOS 11.4.1; Scale/2.00)', 'Token': self._token }
        payload = {'powerStationId': self._system_id}
        r = self._post(self.prefix + 'PowerStation/GetMonitorDetailByPowerstationId',headers= headers, payload=payload)
        self.inverterData = r.json()['data']['inverter'][0]

    def get_power(self):
        return self.inverterData['out_pac']
 
    def get_daily_kwh(self):
        return self.inverterData['eday']

    def get_total_kwh(self):
        return self.inverterData['etotal']