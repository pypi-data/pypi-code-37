# encoding:utf-8
import json
import math
import random
import traceback
from multiprocessing import Semaphore
from queue import Queue
from threading import Thread
import re
import requests
from bs4 import BeautifulSoup
from gzqzl.jianzhu_etl import jianzhu_est_html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from zhulong5.util.fake_useragent import UserAgent



_name_ = "jianzhu"


sema=Semaphore(1)

def get_data(soup, proxies):
    divs = soup.find('div', class_='clearfix')
    sf = divs.find('a', attrs={"sf":"pagebar"})['sf:data']
    total = int(re.findall(r'tt:(\d+),', sf)[0])
    if total != 0:
        total_num = math.ceil(total / 25)
    else:
        return '暂未查询到已登记入库信息'
    action = soup.find('form', class_='pagingform')['action']
    link = 'http://jzsc.mohurd.gov.cn' + action
    form = soup.find('div', class_='clearfix').script.text.replace(' ','')
    total = int(re.findall(r'total":(\d+),', form)[0])
    reload = int(re.findall(r'reload":(\d+),', form)[0])
    pgsz = int(re.findall(r'pgsz":(\d+)', form)[0])
    data_dict={'link':link,'total':total,'reload':reload,'pgsz':pgsz}
    list11 = []
    for dt in range(1, int(total_num)+1):
        tnum = 5
        while tnum > 0:
            tnum -= 1
            r = get_total_data(data_dict, dt, proxies)
            if r:
                list11.append(r)
                break
    if list11 and 'null' not in list11 and 'false' not in list11:
        list2 = json.dumps(list11, ensure_ascii=False)
        return list2
    else:
        raise ValueError


def get_total_data(data_dict, dt, proxies):
    total = data_dict['total']
    reload = data_dict['reload']
    pgsz = data_dict['pgsz']
    link = data_dict['link']
    payloadData = {
        "$total": total,
        "$reload": reload,
        "$pg": dt,
        "$pgsz": pgsz,
    }
    user_agents = UserAgent()
    user_agent = user_agents.chrome
    headers = {
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': user_agent,
    }
    timeOut = 60
    res = requests.post(url=link, headers=headers, data=payloadData, timeout=timeOut, proxies=proxies)
    # 需要判断是否为登录后的页面
    if res.status_code != 200:
        raise ConnectionError
    html = res.text
    soups = BeautifulSoup(html, 'html.parser')
    trs = soups.find('table')
    if soups.find('table'):
        if "暂未查询到已登记入库信息" in soups.find('table').text.replace(' ',''):
            print('requests请求失败！')
            raise ValueError
        else:
            dt_dict = {'pg':dt,'trs':str(trs)}
            dt_dict = json.dumps(dt_dict, ensure_ascii=False)
            return dt_dict
    else:raise ValueError



def get_ip():
    sema.acquire()
    try:
        url="""http://ip.11jsq.com/index.php/api/entry?method=proxyServer.generate_api_url&packid=0&fa=0&fetch_key=&qty=1&time=1&pro=&city=&port=1&format=txt&ss=1&css=&dt=1&specialTxt=3&specialJson="""
        r=requests.get(url)
        time.sleep(1)
        ip=r.text
    except:
        ip="ip失败"
    finally:
        sema.release()
    return ip




def get_f4_data(link, proxies):
    user_agents = UserAgent()
    user_agent = user_agents.chrome
    headers = {
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': user_agent,
        }
    timeOut = 120
    res = requests.get(url=link, headers=headers, timeout=timeOut, proxies=proxies)
    # 需要判断是否为登录后的页面
    if res.status_code != 200:
        raise ConnectionError
    html = res.text
    soups = BeautifulSoup(html, 'html.parser')
    trs = soups.find('body')
    if trs:
        return str(trs)
    else:raise ValueError






def f4(driver, arr, proxies):
    # arr = arr.tolist()
    qyzzzg, zcry, gcxm, blxw, lhxw, hmdjl, sxlhcjjl, bgjl = None, None, None, None, None, None, None, None
    data = []
    href = arr[0]
    page = arr[1]
    # 获取企业资格等详细信息
    driver.get(href)
    locator = (By.XPATH, "//table[@class='pro_table_box datas_table'][string-length()>30]")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
    locator = (By.XPATH, "//ul[@class='tinyTab datas_tabs'][string-length()>20]")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    list_1 = soup.find('ul', class_='tinyTab datas_tabs')
    list_name = []
    for lis in list_1.find_all('li'):
        li = lis.find('a')
        if li.find('em'):
            li.find('em').extract()

        span = li.find('span').text.replace(' ','')
        link = li['data-url']
        if span and link:
            data_dict = {'name':span,'link':link}
            list_name.append(data_dict)


    for li in list_name:
        name = li['name']
        link = 'http://jzsc.mohurd.gov.cn' + li['link']
        if '企业资质资格' in name:
            qyzzzg = get_qyzzzg(link, proxies)
            if not qyzzzg:raise ValueError
        elif '注册人员' in name:
            zcry = get_zcry(link, proxies)
            if not zcry:raise ValueError
        elif '工程项目' in name:
            gcxm = get_gcxm(link, proxies)
            if not gcxm: raise ValueError
        elif '不良行为' in name:
            blxw = get_blxw(link, proxies)
            if not blxw:raise ValueError
        elif '良好行为' in name:
            lhxw = get_lhxw(link, proxies)
            if not lhxw:raise ValueError
        elif '黑名单记录' in name:
            hmdjl = get_hmdjl(link, proxies)
            if not hmdjl: raise ValueError
        elif '失信联合惩戒记录' in name:
            sxlhcjjl = get_sxlhcjjl(link, proxies)
            if not sxlhcjjl:raise ValueError
        elif '变更记录' in name:
            bgjl = get_bgjl(link, proxies)
            if not bgjl: raise ValueError
    tmp = [href, page,qyzzzg,zcry,gcxm,blxw,lhxw,hmdjl,sxlhcjjl,bgjl]
    return tmp


# 企业资质资格
def get_qyzzzg(link, proxies):
    dat1 = get_f4_data(link, proxies)
    soup1 = BeautifulSoup(dat1, 'html.parser')
    if soup1.find('div', class_='clearfix'):
        qyzzzg = get_data(soup1, proxies)
        return qyzzzg
    qyzzzg = soup1.find('table', id='catabled')
    if "暂未查询到已登记入库信息" in qyzzzg.text.replace(' ', ''):
        dat1 = get_f4_data(link, proxies)
        soup1 = BeautifulSoup(dat1, 'html.parser')
        qyzzzg = soup1.find('table', id='catabled')
        if "暂未查询到已登记入库信息" in qyzzzg.text.replace(' ', ''):
            qyzzzg = "暂未查询到已登记入库信息"
    else:
        soup1 = BeautifulSoup(dat1, 'html.parser')
        if soup1.find('td', attrs={'data-header':'资质证书号'}):
            qyzzzg = soup1.find('table', id='catabled')
        else:raise ValueError
    return qyzzzg

# 注册人员
def get_zcry(link, proxies):
    dat2 = get_f4_data(link, proxies)
    soup2 = BeautifulSoup(dat2, 'html.parser')
    if soup2.find('div', class_='clearfix'):
        zcry = get_data(soup2, proxies)
        return zcry
    zcry = soup2.find('table', class_='pro_table_box pro_table_borderright')
    if "暂未查询到已登记入库信息" in zcry.text.replace(' ',''):
        soup2 = BeautifulSoup(dat2, 'html.parser')
        zcry = soup2.find('table', class_='pro_table_box pro_table_borderright')
        if "暂未查询到已登记入库信息" in zcry.text.replace(' ', ''):
            zcry = "暂未查询到已登记入库信息"
    else:
        soup2 = BeautifulSoup(dat2, 'html.parser')
        if soup2.find('td', attrs={'data-header': '注册类别'}):
            zcry = soup2.find('table', class_='pro_table_box pro_table_borderright')
        else:raise ValueError
    return zcry

# 工程项目
def get_gcxm(link, proxies):
    dat3 = get_f4_data(link, proxies)
    soup3 = BeautifulSoup(dat3, 'html.parser')
    if soup3.find('div', class_='clearfix'):
        gcxm = get_data(soup3, proxies)
        return gcxm
    gcxm = soup3.find('table', class_='pro_table_box pro_table_borderright')
    if "暂未查询到已登记入库信息" in gcxm.text.replace(' ',''):
        dat3 = get_f4_data(link, proxies)
        soup3 = BeautifulSoup(dat3, 'html.parser')
        gcxm = soup3.find('table', class_='pro_table_box pro_table_borderright')
        if "暂未查询到已登记入库信息" in gcxm.text.replace(' ', ''):
            gcxm = "暂未查询到已登记入库信息"
    else:
        soup3 = BeautifulSoup(dat3, 'html.parser')
        if soup3.find('td', attrs={'data-header': '项目编码'}):
            gcxm = soup3.find('table', class_='pro_table_box pro_table_borderright')
        else:raise ValueError
    return gcxm

# 不良行为
def get_blxw(link, proxies):
    dat4 = get_f4_data(link, proxies)
    soup4 = BeautifulSoup(dat4, 'html.parser')
    if soup4.find('div', class_='clearfix'):
        blxw = get_data(soup4, proxies)
        return blxw
    blxw = soup4.find('table', class_='pro_table_box pro_table_borderright')
    if "暂未查询到已登记入库信息" in blxw.text.replace(' ',''):
        dat4 = get_f4_data(link, proxies)
        soup4 = BeautifulSoup(dat4, 'html.parser')
        blxw = soup4.find('table', class_='pro_table_box pro_table_borderright')
        if "暂未查询到已登记入库信息" in blxw.text.replace(' ', ''):
            blxw = "暂未查询到已登记入库信息"
    else:
        soup4 = BeautifulSoup(dat4, 'html.parser')
        if soup4.find('td', attrs={'data-header': '诚信记录编号'}):
            blxw = soup4.find('table', class_='pro_table_box pro_table_borderright')
        else:raise ValueError
    return blxw

# 良好行为
def get_lhxw(link, proxies):
    dat5 = get_f4_data(link, proxies)
    soup5 = BeautifulSoup(dat5, 'html.parser')
    if soup5.find('div', class_='clearfix'):
        lhxw = get_data(soup5, proxies)
        return lhxw
    lhxw = soup5.find('table', class_='pro_table_box pro_table_borderright')
    if "暂未查询到已登记入库信息" in lhxw.text.replace(' ',''):
        dat5 = get_f4_data(link, proxies)
        soup5 = BeautifulSoup(dat5, 'html.parser')
        lhxw = soup5.find('table', class_='pro_table_box pro_table_borderright')
        if "暂未查询到已登记入库信息" in lhxw.text.replace(' ', ''):
            lhxw = "暂未查询到已登记入库信息"
    else:
        soup5 = BeautifulSoup(dat5, 'html.parser')
        if soup5.find('td', attrs={'data-header': '诚信记录编号'}):
            lhxw = soup5.find('table', class_='pro_table_box pro_table_borderright')
        else:raise ValueError
    return lhxw

# 黑名单记录
def get_hmdjl(link, proxies):
    dat6 = get_f4_data(link, proxies)
    soup6 = BeautifulSoup(dat6, 'html.parser')
    if soup6.find('div', class_='clearfix'):
        hmdjl = get_data(soup6, proxies)
        return hmdjl
    hmdjl = soup6.find('table', class_='table_box credit_table')
    if "暂未查询到已登记入库信息" in hmdjl.text.replace(' ',''):
        dat6 = get_f4_data(link, proxies)
        soup6 = BeautifulSoup(dat6, 'html.parser')
        hmdjl = soup6.find('table', class_='table_box credit_table')
        if "暂未查询到已登记入库信息" in hmdjl.text.replace(' ', ''):
            hmdjl = "暂未查询到已登记入库信息"
    else:
        soup6 = BeautifulSoup(dat6, 'html.parser')
        if soup6.find('td', attrs={'data-header': '黑名单记录编号'}):
            hmdjl = soup6.find('table', class_='table_box credit_table')
        else:raise ValueError
    return hmdjl

# 失信联合惩戒记录
def get_sxlhcjjl(link, proxies):
    dat7 = get_f4_data(link, proxies)
    soup7 = BeautifulSoup(dat7, 'html.parser')
    if soup7.find('div', class_='clearfix'):
        sxlhcjjl = get_data(soup7, proxies)
        return sxlhcjjl
    sxlhcjjl = soup7.find('table', class_='table_box credit_table')
    if "暂未查询到已登记入库信息" in sxlhcjjl.text.replace(' ',''):
        dat7 = get_f4_data(link, proxies)
        soup7 = BeautifulSoup(dat7, 'html.parser')
        sxlhcjjl = soup7.find('table', class_='table_box credit_table')
        if "暂未查询到已登记入库信息" in sxlhcjjl.text.replace(' ', ''):
            sxlhcjjl = "暂未查询到已登记入库信息"
    else:
        soup7 = BeautifulSoup(dat7, 'html.parser')
        if soup7.find('td', attrs={'data-header': '失信记录编号'}):
            sxlhcjjl = soup7.find('table', class_='table_box credit_table')
        else:raise ValueError
    return sxlhcjjl

# 变更记录
def get_bgjl(link, proxies):
    dat8 = get_f4_data(link, proxies)
    soup8 = BeautifulSoup(dat8, 'html.parser')
    if soup8.find('div', class_='clearfix'):
        bgjl = get_data(soup8, proxies)
        return bgjl
    bgjl = soup8.find('table', class_='pro_table_box')
    if "暂未查询到已登记入库信息" in bgjl.text.replace(' ',''):
        dat8 = get_f4_data(link, proxies)
        soup8 = BeautifulSoup(dat8, 'html.parser')
        bgjl = soup8.find('table', class_='pro_table_box')
        if "暂未查询到已登记入库信息" in bgjl.text.replace(' ', ''):
            bgjl = "暂未查询到已登记入库信息"
    else:
        soup8 = BeautifulSoup(dat8, 'html.parser')
        if soup8.find('td', attrs={'data-header': '变更日期'}):
            bgjl = soup8.find('table', class_='pro_table_box')
        else:raise ValueError
    return bgjl
            



dd = ['href','page','qyzzzg','zcry','gcxm','blxw','lhxw','hmdjl','sxlhcjjl','bgjl']

def work(conp, **args):
    jianzhu_est_html(conp, f=f4, data=dd, **args)


if __name__ == '__main__':
    work(conp=["postgres", "since2015", "192.168.3.171", "guoziqiang", "jianzhu"],datloadtimeout=180,num=150)

    # driver=webdriver.Chrome()
    # driver.get('https://www.baidu.com')
    # ip = get_ip()
    # print("本次ip %s" % ip)
    # if re.match("[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}:[0-9]{1,5}", ip) is None:
    #     print("ip不合法")
    #
    # df = f4(driver,['http://jzsc.mohurd.gov.cn/dataservice/query/comp/compDetail/001607220057242166','gg'],proxies = {
    #                 "http": "http://%s" % (ip),})
    # # df = get_f4_data('http://jzsc.mohurd.gov.cn/dataservice/query/comp/caDetailList/001607220057213108', proxies = {"http": "http://%s" % (ip),})
    # print(df)