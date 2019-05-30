#最通用的时间解析

import re 

from bs4 import BeautifulSoup

from lmf.dbv2 import db_query



def get_page(url,quyu):
    db,schema=quyu.split('_')
    sql="""select page from %s.gg_html  where href='%s'
    """%(schema,url)
    conp=['postgres','since2015','192.168.4.175',db,schema]
    df=db_query(sql,dbtype='postgresql',conp=conp)
    if df.empty :
        return None
    else :
        return df.iat[0,0]


def extime(page):
    if page is None:  
        return None
    soup=BeautifulSoup(page,'lxml')
    
    txt=re.sub('[^\u4E00-\u9Fa5a-zA-Z0-9:：\-\\/]','',soup.text)
    patterns=[r'(?:发[布稿]|信息)(?:日期|时间)[:：](20[0-1][0-9])[\-/\\年]([0-1]?[0-9])[\-/\\月]([0-3]?[0-9])[日]?(?:(\d{1,2})[:：](\d{1,2})(?:[:：](\d{1,2})|)|)'
        ]
    for p in patterns:
        a=re.findall(p,txt)
        if a !=[] and a[0][3]!='':
            return '-'.join(a[0][:3])+' '+':'.join(a[0][3:])
        if a !=[] and a[0][3]=='':
            return '-'.join(a[0][:3])
    return None



