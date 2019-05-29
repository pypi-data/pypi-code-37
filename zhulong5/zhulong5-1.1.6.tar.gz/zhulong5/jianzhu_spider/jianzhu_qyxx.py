# encoding:utf-8
import json
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

def get_data(driver, soup):
    # div = soup.find('div', class_='quotes')
    # total_num = div.find('a', class_='nxt')['dt']
    # if total_num == None:
    #     total_num = div.find_all('a')[-1]['dt']
    divs = soup.find('div', class_='clearfix')
    a = divs.find('a', attrs={"sf":"pagebar"})['sf:data']
    total = re.findall(r'tt:(\d+),', a)[0]
    total = int(total)
    if total != 0:
        if total / 25 == int(total / 25):
            total_num = int(total / 25)
        else:
            total_num = int(total / 25) + 1
    else:
        raise ValueError
    action = soup.find('form', class_='pagingform')['action']
    link = 'http://jzsc.mohurd.gov.cn' + action
    form = soup.find('div', class_='clearfix').script.text.replace(' ','')
    # form = '__pgfm('',{"$total":621,"$reload":0,"$pg":2,"$pgsz":25})'
    total = int(re.findall(r'total":(\d+),', form)[0])
    reload = int(re.findall(r'reload":(\d+),', form)[0])
    pgsz = int(re.findall(r'pgsz":(\d+)', form)[0])
    data_dict={'link':link,'total':total,'reload':reload,'pgsz':pgsz}
    ip = get_ip()
    print("本次ip %s" % ip)
    if re.match("[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}:[0-9]{1,5}", ip) is None:
        print("ip不合法")
        raise ValueError
    try:
        proxies = {"http": "http://%s"%(ip)}
    except Exception as e:
        traceback.print_exc()
        raise ValueError
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
    timeOut = 120
    time.sleep(random.uniform(1, 2))
    res = requests.post(url=link, headers=headers, data=payloadData, timeout=timeOut, proxies=proxies)
    # 需要判断是否为登录后的页面
    if res.status_code != 200:
        raise ConnectionError
    else:
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



def f4(driver, arr):
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
        list_name.append(span)
    # print(list_name)
    # 企业资质资格
    if '企业资质资格' in list_name:
        driver.find_element_by_xpath("//ul[@class='tinyTab datas_tabs']/li/a[contains(string(), '企业资质资格')]").click()
        locator = (By.XPATH, "//ul[@class='tinyTab datas_tabs']/li[@class='activeTinyTab']/a[contains(string(), '企业资质资格')]")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        time.sleep(random.uniform(1, 2))
        locator = (By.XPATH, "//table[@id='catabled'][string-length()>12]")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        soup1 = BeautifulSoup(driver.page_source, 'html.parser')
        # time.sleep(random.uniform(3, 4))
        if soup1.find('div', class_='quotes'):
            sp = soup1.find('table', id='catabled')
            qyzzzg = get_data(driver, sp)
        else:
            qyzzzg = soup1.find('table', id='catabled')
            if "暂未查询到已登记入库信息" in qyzzzg.text.replace(' ', ''):
                qyzzzg = "暂未查询到已登记入库信息"
            else:
                locator = (By.XPATH, "//td[@data-header='资质证书号'][string-length()>2]")
                WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
                soup1 = BeautifulSoup(driver.page_source, 'html.parser')
                qyzzzg = soup1.find('table', id='catabled')

    # 注册人员
    src = driver.find_element_by_xpath("//iframe[@class='datalist']").get_attribute('src')[-50:]
    iframe = driver.find_element_by_xpath("//iframe[@class='datalist']")
    if '注册人员' in list_name:
        driver.find_element_by_xpath("//ul[@class='tinyTab datas_tabs']/li/a[contains(string(), '注册人员')]").click()
        locator = (By.XPATH, "//ul[@class='tinyTab datas_tabs']/li[@class='activeTinyTab']/a[contains(string(), '注册人员')]")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        src = driver.find_element_by_xpath("//iframe[@class='datalist']").get_attribute('src')[-50:]
        driver.switch_to.frame(iframe)
        time.sleep(random.uniform(1, 2))
        locator = (By.XPATH, "//table[@class='pro_table_box pro_table_borderright'][string-length()>12]")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        soup2 = BeautifulSoup(driver.page_source, 'html.parser')
        if soup2.find('div', class_='quotes'):
            sp = soup2.find('body')
            zcry = get_data(driver, sp)
        else:
            zcry = soup2.find('table', class_='pro_table_box pro_table_borderright')
            if "暂未查询到已登记入库信息" in zcry.text.replace(' ',''):
                zcry = "暂未查询到已登记入库信息"
            else:
                locator = (By.XPATH, "//td[@data-header='注册类别'][string-length()>2]")
                WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
                soup2 = BeautifulSoup(driver.page_source, 'html.parser')
                zcry = soup2.find('table', class_='pro_table_box pro_table_borderright')
        driver.switch_to.default_content()

    # 工程项目
    if '工程项目' in list_name:
        driver.find_element_by_xpath("//ul[@class='tinyTab datas_tabs']/li/a[contains(string(), '工程项目')]").click()
        locator = (By.XPATH, "//ul[@class='tinyTab datas_tabs']/li[@class='activeTinyTab']/a[contains(string(), '工程项目')]")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        locator = (By.XPATH, "//iframe[@class='datalist'][not(contains(@src, '%s'))]"%src)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        src = driver.find_element_by_xpath("//iframe[@class='datalist']").get_attribute('src')[-50:]

        driver.switch_to.frame(iframe)
        time.sleep(random.uniform(1, 2))
        locator = (By.XPATH, "//table[@class='pro_table_box pro_table_borderright'][string-length()>12]")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        soup3 = BeautifulSoup(driver.page_source, 'html.parser')
        if soup3.find('div', class_='quotes'):
            sp = soup3.find('body')
            gcxm = get_data(driver, sp)
        else:
            gcxm = soup3.find('table', class_='pro_table_box pro_table_borderright')
            if "暂未查询到已登记入库信息" in gcxm.text.replace(' ',''):
                gcxm = "暂未查询到已登记入库信息"
            else:
                locator = (By.XPATH, "//td[@data-header='项目编码'][string-length()>2]")
                WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
                soup3 = BeautifulSoup(driver.page_source, 'html.parser')
                gcxm = soup3.find('table', class_='pro_table_box pro_table_borderright')
        driver.switch_to.default_content()

    # 不良行为
    if '不良行为' in list_name:
        driver.find_element_by_xpath("//ul[@class='tinyTab datas_tabs']/li/a[contains(string(), '不良行为')]").click()
        locator = (By.XPATH, "//ul[@class='tinyTab datas_tabs']/li[@class='activeTinyTab']/a[contains(string(), '不良行为')]")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))

        locator = (By.XPATH, "//iframe[@class='datalist'][not(contains(@src, '%s'))]"%src)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        src = driver.find_element_by_xpath("//iframe[@class='datalist']").get_attribute('src')[-50:]

        driver.switch_to.frame(iframe)
        time.sleep(random.uniform(1, 2))
        locator = (By.XPATH, "//table[@class='pro_table_box pro_table_borderright'][string-length()>12]")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        soup4 = BeautifulSoup(driver.page_source, 'html.parser')
        if soup4.find('div', class_='quotes'):
            sp = soup4.find('body')
            blxw = get_data(driver, sp)
        else:
            blxw = soup4.find('table', class_='pro_table_box pro_table_borderright')
            if "暂未查询到已登记入库信息" in blxw.text.replace(' ',''):
                blxw = "暂未查询到已登记入库信息"
            else:
                locator = (By.XPATH, "//td[@data-header='诚信记录编号'][string-length()>2]")
                WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
                soup4 = BeautifulSoup(driver.page_source, 'html.parser')
                blxw = soup4.find('table', class_='pro_table_box pro_table_borderright')
        driver.switch_to.default_content()

    # 良好行为
    if '良好行为' in list_name:
        driver.find_element_by_xpath("//ul[@class='tinyTab datas_tabs']/li/a[contains(string(), '良好行为')]").click()
        locator = (By.XPATH, "//ul[@class='tinyTab datas_tabs']/li[@class='activeTinyTab']/a[contains(string(), '良好行为')]")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))

        locator = (By.XPATH, "//iframe[@class='datalist'][not(contains(@src, '%s'))]"%src)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        src = driver.find_element_by_xpath("//iframe[@class='datalist']").get_attribute('src')[-50:]

        driver.switch_to.frame(iframe)
        time.sleep(random.uniform(1, 2))
        locator = (By.XPATH, "//table[@class='pro_table_box pro_table_borderright'][string-length()>12]")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        soup5 = BeautifulSoup(driver.page_source, 'html.parser')
        if soup5.find('div', class_='quotes'):
            sp = soup5.find('body')
            lhxw = get_data(driver, sp)
        else:
            lhxw = soup5.find('table', class_='pro_table_box pro_table_borderright')
            if "暂未查询到已登记入库信息" in lhxw.text.replace(' ',''):
                lhxw = "暂未查询到已登记入库信息"
            else:
                locator = (By.XPATH, "//table[@class='pro_table_box pro_table_borderright'][string-length()>30]")
                WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
                soup5 = BeautifulSoup(driver.page_source, 'html.parser')
                lhxw = soup5.find('table', class_='pro_table_box pro_table_borderright')
        driver.switch_to.default_content()

    # 黑名单记录
    if '黑名单记录' in list_name:
        driver.find_element_by_xpath("//ul[@class='tinyTab datas_tabs']/li/a[contains(string(), '黑名单记录')]").click()
        locator = (By.XPATH, "//ul[@class='tinyTab datas_tabs']/li[@class='activeTinyTab']/a[contains(string(), '黑名单记录')]")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))

        locator = (By.XPATH, "//iframe[@class='datalist'][not(contains(@src, '%s'))]"%src)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        src = driver.find_element_by_xpath("//iframe[@class='datalist']").get_attribute('src')[-50:]

        driver.switch_to.frame(iframe)
        time.sleep(random.uniform(1, 2))
        locator = (By.XPATH, "//table[@class='table_box credit_table'][string-length()>12]")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        soup6 = BeautifulSoup(driver.page_source, 'html.parser')
        if soup6.find('div', class_='quotes'):
            sp = soup6.find('body')
            hmdjl = get_data(driver, sp)
        else:
            hmdjl = soup6.find('table', class_='table_box credit_table')
            if "暂未查询到已登记入库信息" in hmdjl.text.replace(' ',''):
                hmdjl = "暂未查询到已登记入库信息"
            else:
                locator = (By.XPATH, "//table[@class='table_box credit_table'][string-length()>30]")
                WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
                soup6 = BeautifulSoup(driver.page_source, 'html.parser')
                hmdjl = soup6.find('table', class_='table_box credit_table')
        driver.switch_to.default_content()

    # 失信联合惩戒记录
    if '失信联合惩戒记录' in list_name:
        driver.find_element_by_xpath("//ul[@class='tinyTab datas_tabs']/li/a[contains(string(), '失信联合惩戒记录')]").click()
        locator = (By.XPATH, "//ul[@class='tinyTab datas_tabs']/li[@class='activeTinyTab']/a[contains(string(), '失信联合惩戒记录')]")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))

        locator = (By.XPATH, "//iframe[@class='datalist'][not(contains(@src, '%s'))]"%src)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        src = driver.find_element_by_xpath("//iframe[@class='datalist']").get_attribute('src')[-50:]

        driver.switch_to.frame(iframe)
        time.sleep(random.uniform(1, 2))
        locator = (By.XPATH, "//table[@class='table_box credit_table'][string-length()>12]")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        soup7 = BeautifulSoup(driver.page_source, 'html.parser')
        if soup7.find('div', class_='quotes'):
            sp = soup7.find('body')
            sxlhcjjl = get_data(driver, sp)
        else:
            sxlhcjjl = soup7.find('table', class_='table_box credit_table')
            if "暂未查询到已登记入库信息" in sxlhcjjl.text.replace(' ',''):
                sxlhcjjl = "暂未查询到已登记入库信息"
            else:
                locator = (By.XPATH, "//table[@class='table_box credit_table'][string-length()>30]")
                WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
                soup7 = BeautifulSoup(driver.page_source, 'html.parser')
                sxlhcjjl = soup7.find('table', class_='table_box credit_table')
        driver.switch_to.default_content()

    # 变更记录
    if '变更记录' in list_name:
        driver.find_element_by_xpath("//ul[@class='tinyTab datas_tabs']/li/a[contains(string(), '变更记录')]").click()
        locator = (By.XPATH, "//ul[@class='tinyTab datas_tabs']/li[@class='activeTinyTab']/a[contains(string(), '变更记录')]")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        locator = (By.XPATH, "//iframe[@class='datalist'][not(contains(@src, '%s'))]"%src)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        src = driver.find_element_by_xpath("//iframe[@class='datalist']").get_attribute('src')[-50:]

        driver.switch_to.frame(iframe)
        time.sleep(random.uniform(1, 2))
        locator = (By.XPATH, "//table[@class='pro_table_box'][string-length()>12]")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        soup8 = BeautifulSoup(driver.page_source, 'html.parser')
        if soup8.find('div', class_='quotes'):
            sp = soup8.find('body')
            bgjl = get_data(driver, sp)
        else:
            bgjl = soup8.find('table', class_='pro_table_box')
            if "暂未查询到已登记入库信息" in bgjl.text.replace(' ',''):
                bgjl = "暂未查询到已登记入库信息"
            else:
                locator = (By.XPATH, "//table[@class='pro_table_box'][string-length()>30]")
                WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
                soup8 = BeautifulSoup(driver.page_source, 'html.parser')
                bgjl = soup8.find('table', class_='pro_table_box')
        driver.switch_to.default_content()

    tmp = [href,page,qyzzzg,zcry,gcxm,blxw,lhxw,hmdjl,sxlhcjjl,bgjl]
    # data.append(tmp)
    # print('成功！')
    return tmp

dd = ['href','page','qyzzzg','zcry','gcxm','blxw','lhxw','hmdjl','sxlhcjjl','bgjl']

def work(conp, **args):
    jianzhu_est_html(conp, f=f4, data=dd, **args)


if __name__ == '__main__':
    work(conp=["postgres", "since2015", "192.168.3.171", "guoziqiang", "jianzhu"],pageloadtimeout=180,num=150)

    # driver=webdriver.Chrome()
    # driver.get('https://www.baidu.com')
    #
    # df = f4(driver,['http://jzsc.mohurd.gov.cn/dataservice/query/comp/compDetail/001607220057198419',0])
    # print(df)