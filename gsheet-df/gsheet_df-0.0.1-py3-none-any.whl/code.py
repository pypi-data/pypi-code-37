import requests
import pandas as pd
from io import StringIO

def download(url, table, element_sep = '@', row_sep = '\n', auth='', str_only=False):
    """
    download(url, table, element_sep = '@', row_sep = '\n', auth='', str_only=False)
    
    url: the url of googlesheet
    table: names of tables, separated by ','
    auth: secret key for authentication
    srt_only: return csv text instead of pd.dataframe
    """
    data = {
        'auth': auth,
        'table': table,
        'elementsep': element_sep,
        'rowsep': row_sep,
    }
    response = requests.post(url, data=data)
    if str_only:
        return response.text
    else:
        return pd.read_csv(StringIO(response.text), sep=element_sep)
