from lmf.dbv2 import db_write ,db_query
import sys 
from lmfgg.table.common import tb1,tb2,fm
from lmfgg.txt import ismat
from bs4 import BeautifulSoup
from lmfgg.ps.common import ps,getwordfdb
from lmfgg.table import ext1,ext2,ext3
from lmfgg.common import getpage 
from lmfgg.getdata import initwords_ol
from lmfgg.txt import ismat
from lmfgg.ps.common import pat
from lmfgg.getdata import extpage_ol
from lmfgg.ps.psdata import psext
from lmfgg.getdata import getsist
from bs4 import  BeautifulSoup
from lmfgg.common import to_arr
from lmfgg.ps.pspre import get_pure_ps
from collections import OrderedDict
import re 
import copy
krr,krrdict=initwords_ol()
sql="select page from v.gg_html where quyu= 'hunan_shaoyang' and href='http://ggzy.shaoyang.gov.cn/新流程/招投标信息/jyxx_1.aspx?iq=x&type=中标公示&tpid=5b90d568f0480600d4a602a1' "

df=db_query(sql,dbtype="postgresql",conp=["gpadmin",'since2015','192.168.4.179','base_db','v'])
#page=getpage("http://ggzy.shaoyang.gov.cn/新流程/招投标信息/jyxx_1.aspx?iq=x&type=中标公示&tpid=5b90d568f0480600d4a602a1","hunan_shaoyang")
page=df.at[0,'page']
soup=BeautifulSoup(page,'lxml')
data=extpage_ol(page)




# df1['data']=df1['ps'].map(lambda x:ps(x,krr))

# for w in df1['data']:print(w)

# for w in df1['href'][:10]:print(w)
