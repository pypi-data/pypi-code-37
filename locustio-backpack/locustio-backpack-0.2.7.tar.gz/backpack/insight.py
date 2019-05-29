import pandas as pd
import numpy as np
from locust import runners
from time import sleep
from json import dumps, loads
import requests
from ast import literal_eval

from .display import WARN, DEBUG
from .web import run_reporter
from .options import Options



class Insight(object):
    singleton = False

    def __init__(self, LEC):
        self.collection = LEC()
        self.container = self.collection.endpoint_statistics
        self.deserialize_frames()
        self.n_requests = self.collection.totals
        colorder = ['Name', 'Calls', 'API_Usage', 
                    'Success_Rate', 'Median', 
                    'Percentile_95', 'Quartile_Q1', 
                    'Quartile_Q3', 'IQR']

        self.data = {
            'Name' : [],
            'Calls': [],
            'API_Usage': [],
            'Success_Rate': [],
            'Percentile_95':[],
            'Quartile_Q1': [],
            'Median': [],
            'Quartile_Q3': [],
            'IQR': []
        }

        self.insights = list()
        for frame in self.container:
            df = self.container[frame]
            df.name = frame
            self.insights.append(df)

            calls   = self.i_call_count(df)
            usage   = self.i_api_usage(calls)
            s_rate  = self.i_success_rate(df, calls)
            percentile = self.i_percentile(df)
            quartile_gen = self.i_quartile(df)
            Q1      = next(quartile_gen)
            med     = next(quartile_gen)
            Q3      = next(quartile_gen)

            self.data['Name'].append(frame)
            self.data['Calls'].append(calls)
            self.data['API_Usage'].append(usage)
            self.data['Success_Rate'].append(s_rate)
            self.data['Percentile_95'].append(percentile)
            self.data['Quartile_Q1'].append(Q1)
            self.data['Median'].append(med)
            self.data['Quartile_Q3'].append(Q3)
            self.data['IQR'].append(round(Q3 - Q1, 3))
        
        final = pd.DataFrame(self.data)
        final = final[colorder]

        if Options.save_test_csvs == True:
            self.save_data(final)

        if Options.web_report == True:
            run_reporter(final, self.insights)


    def save_data(self, final):
        final.to_csv(path_or_buf='global_stats.csv', index=False)
        for framecat in self.insights:
            self.insights[framecat].to_csv(path_or_buf='{}_stats.csv'.format(str(framecat)), index=False)

    
    def i_call_count(self, df):
        return len(df.index)

    def i_api_usage(self, callcount):
        return round((float(callcount) / float(self.n_requests)) * 100.0, 1)

    def i_success_rate(self, df, calls):
        n_success   = len(df[(df['status'] == True)].index)
        return round((float(n_success) / float(calls)) * 100.0, 1)

    def i_percentile(self, df):
        return round(np.percentile(df.response_time, 95), 3)

    def i_quartile(self, df):
        for x in [25, 50, 75]:
            yield round(np.percentile(df.response_time, x), 3)

    def deserialize_frames(self):
        if not self.collection.distrib: return

        def deserialize(obj):
            newdict = dict()
            for client in obj:
                for endp in obj[client]:
                    df = pd.DataFrame.from_dict(obj[client][endp])
                    if endp in newdict:
                        union = pd.concat([newdict[endp], df])
                        newdict[endp] = union
                    else:
                        newdict[endp] = df

            self.container = newdict
        
        try:
            req = requests.get("http://{}:8089/backpack".format(runners.locust_runner.options.master_host))
            serial_frames = loads(req.content)

            req_clients = requests.get("http://{}:8089/stats/requests".format(runners.locust_runner.options.master_host))
            n_clients = len(loads(req_clients.content)["slaves"])


            while len(serial_frames.keys()) != n_clients:
                sleep(1.5)
                serial_frames = self.retry_backpack_page()
            
        except Exception as e: print(e)
        else: deserialize(serial_frames)

    def retry_backpack_page(self):
        req = requests.get("http://{}:8089/backpack".format(runners.locust_runner.options.master_host))
        serial_frames = loads(req.content)
        return serial_frames


    def __new__(cls, *args, **kwargs):
        if Insight.singleton == False:
            Insight.singleton = True
            return object.__new__(cls, *args, **kwargs)
        return