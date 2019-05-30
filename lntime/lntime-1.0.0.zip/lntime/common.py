#最通用的时间解析

import re 

from bs4 import BeautifulSoup

from lmf.dbv2 import db_query



def get_page(url,quyu):
    db,schema=quyu.split('_')
    sql="""select url,page from %s.gg_html 
    ---- where href='%s'
    """%(schema,url)
    conp=['postgres','since2015','192.168.4.175',db,schema]
    df=db_query(sql,dbtype='postgresql',conp=conp)
    if df.empty :
        return None
    else :
        return df


def extime(page):
    if page is None:
        return None
    lxmlparser='lxml'
    soup=BeautifulSoup(page,lxmlparser)
    
    txt=re.sub('[^\u4E00-\u9Fa5a-zA-Z0-9:：\-\\/]','',soup.text)
    patterns1=[r'发[布稿](?:日期|时间)[:：](20[0-1][0-9])[\-/\\年]([0-1][0-9])[\-/\\月]([0-3][0-9])'
        ]
    patterns2=[r'发[布稿](?:日期|时间)[:：]20[0-1][0-9][\-/\\年][0-1][0-9][\-/\\月][0-3][0-9](\d{1,2})[:：](\d{1,2})[:：](\d{1,2})']
    for p in patterns1:
        a=re.findall(p,txt)
        if a !=[]:
            t1= '-'.join(a[0])
        else:
            t1=''

    for p in patterns2:
        a=re.findall(p,txt)
        if a !=[]:
            t2=':'.join(a[0])
        else:
            t2=''
    if t1 :
        return t1+' '+t2
    else:
        return None



