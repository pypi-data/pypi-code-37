# encoding:utf-8
import json
import random
import traceback
from multiprocessing import Semaphore
from queue import Queue
from threading import Thread
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from zhulong5.util.fake_useragent import UserAgent
from gzqzl.jianzhu_etl import jianzhu_ryxx_est_html

_name_ = "jianzhu"

# --------------------------------------------------------获取多页注册人员内容----------------------------------------------
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

# ---------------------------------------------------------程序主入口------------------------------------------------------

def f7(driver, arr):
    ryxx_href, ryxx_nanme, sex, id_type, id_number, zyzcxx, grgcyj, blxw, lhxw, hmdjl, bgjl = None, None, None, None, None, None, None, None, None, None, None
    href = arr[0]
    ryxx_href = arr[1]
    driver=webdriver.Chrome()
    driver.get(ryxx_href)
    data = []
    try:
        locator = (By.XPATH, "//div[@class='activeTinyTabContent'][string-length()>30]")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
    except:
        driver.refresh()
        locator = (By.XPATH, "//div[@class='activeTinyTabContent'][string-length()>30]")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
    ryxx_name = driver.find_element_by_xpath("//div[@class='user_info spmtop']").text.strip()
    sex = driver.find_element_by_xpath("//dd[@class='query_info_dd1']").text.strip().split('：')[1]
    id_type = driver.find_element_by_xpath("//dd[@class='query_info_dd2'][1]").text.strip().split('：')[1]
    id_number = driver.find_element_by_xpath("//dd[@class='query_info_dd2'][2]").text.strip().split('：')[1]
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
    # 执业注册信息
    if '执业注册信息' in list_name:
        driver.find_element_by_xpath("//ul[@class='tinyTab datas_tabs']/li/a[contains(string(), '执业注册信息')]").click()
        locator = (
            By.XPATH,
            "//ul[@class='tinyTab datas_tabs']/li[@class='activeTinyTab']/a[contains(string(), '执业注册信息')]")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        time.sleep(random.uniform(1, 2))
        locator = (By.XPATH, "//div[@id='regcert_tab'][string-length()>12]")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        soup1 = BeautifulSoup(driver.page_source, 'html.parser')

        if soup1.find('div', class_='quotes'):
            sp = soup1.find('div', id='regcert_tab')
            zyzcxx = get_data(driver, sp)
        else:
            zyzcxx = soup1.find('div', id='regcert_tab')
            if "暂未查询到已登记入库信息" in zyzcxx.text.replace(' ', ''):
                zyzcxx = "暂未查询到已登记入库信息"

    # 个人工程业绩
    src = driver.find_element_by_xpath("//iframe[@class='datalist']").get_attribute('src')[-50:]
    iframe = driver.find_element_by_xpath("//iframe[@class='datalist']")
    if '个人工程业绩' in list_name:
        driver.find_element_by_xpath("//ul[@class='tinyTab datas_tabs']/li/a[contains(string(), '个人工程业绩')]").click()
        locator = (By.XPATH,"//ul[@class='tinyTab datas_tabs']/li[@class='activeTinyTab']/a[contains(string(), '个人工程业绩')]")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        src = driver.find_element_by_xpath("//iframe[@class='datalist']").get_attribute('src')[-50:]
        driver.switch_to.frame(iframe)
        time.sleep(random.uniform(1, 2))
        locator = (By.XPATH, "//table[@class='pro_table_box pro_table_borderright'][string-length()>12]")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        soup2 = BeautifulSoup(driver.page_source, 'html.parser')
        if soup2.find('div', class_='quotes'):
            sp = soup2.find('body')
            grgcyj = get_data(driver, sp)
        else:
            grgcyj = soup2.find('table', class_='pro_table_box pro_table_borderright')
            if "暂未查询到已登记入库信息" in grgcyj.text.replace(' ',''):
                grgcyj = "暂未查询到已登记入库信息"
        driver.switch_to.default_content()

    # 不良行为
    if '不良行为' in list_name:
        driver.find_element_by_xpath("//ul[@class='tinyTab datas_tabs']/li/a[contains(string(), '不良行为')]").click()
        locator = (
            By.XPATH, "//ul[@class='tinyTab datas_tabs']/li[@class='activeTinyTab']/a[contains(string(), '不良行为')]")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        locator = (By.XPATH, "//iframe[@class='datalist'][not(contains(@src, '%s'))]" % src)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))

        src = driver.find_element_by_xpath("//iframe[@class='datalist']").get_attribute('src')[-50:]
        driver.switch_to.frame(iframe)
        time.sleep(random.uniform(1, 2))
        locator = (By.XPATH, "//table[@class='pro_table_box pro_table_borderright'][string-length()>12]")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        soup3 = BeautifulSoup(driver.page_source, 'html.parser')
        if soup3.find('div', class_='quotes'):
            sp = soup3.find('body')
            blxw = get_data(driver, sp)
        else:
            blxw = soup3.find('table', class_='pro_table_box pro_table_borderright')
            if "暂未查询到已登记入库信息" in blxw.text.replace(' ',''):
                blxw = "暂未查询到已登记入库信息"
        driver.switch_to.default_content()

    # 良好行为
    if '良好行为' in list_name:
        driver.find_element_by_xpath("//ul[@class='tinyTab datas_tabs']/li/a[contains(string(), '良好行为')]").click()
        locator = (
            By.XPATH, "//ul[@class='tinyTab datas_tabs']/li[@class='activeTinyTab']/a[contains(string(), '良好行为')]")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))

        locator = (By.XPATH, "//iframe[@class='datalist'][not(contains(@src, '%s'))]" % src)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        src = driver.find_element_by_xpath("//iframe[@class='datalist']").get_attribute('src')[-50:]

        driver.switch_to.frame(iframe)
        time.sleep(random.uniform(1, 2))
        locator = (By.XPATH, "//table[@class='pro_table_box pro_table_borderright'][string-length()>12]")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        soup4 = BeautifulSoup(driver.page_source, 'html.parser')
        if soup4.find('div', class_='quotes'):
            sp = soup4.find('body')
            lhxw = get_data(driver, sp)
        else:
            lhxw = soup4.find('table', class_='pro_table_box pro_table_borderright')
            if "暂未查询到已登记入库信息" in lhxw.text.replace(' ',''):
                lhxw = "暂未查询到已登记入库信息"
        driver.switch_to.default_content()

    # 黑名单记录
    if '黑名单记录' in list_name:
        driver.find_element_by_xpath("//ul[@class='tinyTab datas_tabs']/li/a[contains(string(), '黑名单记录')]").click()
        locator = (
            By.XPATH, "//ul[@class='tinyTab datas_tabs']/li[@class='activeTinyTab']/a[contains(string(), '黑名单记录')]")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))

        locator = (By.XPATH, "//iframe[@class='datalist'][not(contains(@src, '%s'))]" % src)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        src = driver.find_element_by_xpath("//iframe[@class='datalist']").get_attribute('src')[-50:]

        driver.switch_to.frame(iframe)
        time.sleep(random.uniform(1, 2))
        locator = (By.XPATH, "//table[@class='table_box credit_table'][string-length()>12]")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        soup5 = BeautifulSoup(driver.page_source, 'html.parser')
        if soup5.find('div', class_='quotes'):
            sp = soup5.find('body')
            hmdjl = get_data(driver, sp)
        else:
            hmdjl = soup5.find('table', class_='table_box credit_table')
            if "暂未查询到已登记入库信息" in hmdjl.text.replace(' ',''):
                hmdjl = "暂未查询到已登记入库信息"
        driver.switch_to.default_content()

    # 变更记录
    if '变更记录' in list_name:
        driver.find_element_by_xpath("//ul[@class='tinyTab datas_tabs']/li/a[contains(string(), '变更记录')]").click()
        locator = (
            By.XPATH, "//ul[@class='tinyTab datas_tabs']/li[@class='activeTinyTab']/a[contains(string(), '变更记录')]")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        locator = (By.XPATH, "//iframe[@class='datalist'][not(contains(@src, '%s'))]" % src)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))

        driver.switch_to.frame(iframe)
        time.sleep(random.uniform(1, 2))
        locator = (By.XPATH, "//table[@class='pro_table_box'][string-length()>12]")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))
        soup6 = BeautifulSoup(driver.page_source, 'html.parser')
        if soup6.find('div', class_='quotes'):
            sp = soup6.find('body')
            bgjl = get_data(driver, sp)
        else:
            bgjl = soup6.find('table', class_='pro_table_box')
            if "暂未查询到已登记入库信息" in bgjl.text.replace(' ',''):
                bgjl = "暂未查询到已登记入库信息"
        driver.switch_to.default_content()

    tmp = [href, ryxx_href, ryxx_name, sex, id_type, id_number, zyzcxx, grgcyj, blxw, lhxw, hmdjl, bgjl]
    data.append(tmp)
    df = pd.DataFrame(data=data)
    return df


dd = ["href", "ryxx_href", "ryxx_name", "sex", "id_type", "id_number", "zyzcxx", "grgcyj", "blxw", "lhxw", "hmdjl", "bgjl"]

def work(conp, **args):
    jianzhu_ryxx_est_html(conp, f=f7, data=dd, **args)


if __name__ == '__main__':
    work(conp=["postgres", "since2015", "192.168.3.171", "guoziqiang", "jianzhu"], pageloadtimeout=180, num=150)

    # data = ['http://jzsc.mohurd.gov.cn/dataservice/query/comp/compDetail/001607220057358803',
    #         '["{"pg": 1, "trs": "<table class="pro_table_box pro_table_borderright" width="100%">n<colgroup>n<col width="5%"/>n<col width="15%"/>n<col width="20%"/>n<col width="20%"/>n<col width="20%"/>n<col width="20%"/>n</colgroup>n<thead>n<tr>n<th colspan="6" style=" background: #fff; text-align: left;">n<div class="comp_regstaff_links">n<a class="formsubmit selected" data-url="/dataservice/query/comp/regStaffList/001607220057196741/" href="javascript:void(0)">全部<span>（37）</span></a>rntttttrnttttt其中：rntttttrnttttt<a class="formsubmit" data-url="/dataservice/query/comp/regStaffList/001607220057196741/" href="javascript:void(0)" reg_type="RY_ZCLB_071">一级注册建造师<span>（6）</span></a>n<a class="formsubmit" data-url="/dataservice/query/comp/regStaffList/001607220057196741/" href="javascript:void(0)" reg_type="RY_ZCLB_072">二级注册建造师<span>（23）</span></a>n<a class="formsubmit" data-url="/dataservice/query/comp/regStaffList/001607220057196741/" href="javascript:void(0)" reg_type="RY_ZCLB_073">一级临时注册建造师<span>（2）</span></a>n<a class="formsubmit" data-url="/dataservice/query/comp/regStaffList/001607220057196741/" href="javascript:void(0)" reg_type="RY_ZCLB_074">二级临时注册建造师<span>（6）</span></a>n</div>n</th>n</tr>n<tr>n<th>序号</th>n<th>姓名</th>n<th>身份证号</th>n<th>注册类别</th>n<th>注册号（执业印章号）</th>n<th>注册专业</th>n</tr>n</thead>n<tbody>n<tr>n<td data-header="序号">1</td>n<td data-header="姓名" style="font-size: 16px;">n<a href="javascript:void(0)" onclick="top.window.location.href="/dataservice/query/staff/staffDetail/001610081902126905"">杨定武</a>n</td>n<td data-header="身份证号">5329016******21</td>n<td data-header="注册类别">二级临时注册建造师</td>n<td data-header="注册号（执业印章号）">滇204080800077(临)</td>n<td data-header="注册专业">建筑工程</td>n</tr>n<tr>n<td data-header="序号">2</td>n<td data-header="姓名" style="font-size: 16px;">n<a href="javascript:void(0)" onclick="top.window.location.href="/dataservice/query/staff/staffDetail/001610081853022983"">胡兆田</a>n</td>n<td data-header="身份证号">5329016******33</td>n<td data-header="注册类别">二级临时注册建造师</td>n<td data-header="注册号（执业印章号）">滇204090900324(临)</td>n<td data-header="注册专业">市政公用工程</td>n</tr>n<tr>n<td data-header="序号">3</td>n<td data-header="姓名" style="font-size: 16px;">n<a href="javascript:void(0)" onclick="top.window.location.href="/dataservice/query/staff/staffDetail/001610081853021945"">杨全寿</a>n</td>n<td data-header="身份证号">5329016******35</td>n<td data-header="注册类别">二级临时注册建造师</td>n<td data-header="注册号（执业印章号）">滇204090900323(临)</td>n<td data-header="注册专业">建筑工程</td>n</tr>n<tr>n<td data-header="序号">4</td>n<td data-header="姓名" style="font-size: 16px;">n<a href="javascript:void(0)" onclick="top.window.location.href="/dataservice/query/staff/staffDetail/001610081853023593"">杨春源</a>n</td>n<td data-header="身份证号">5329017******41</td>n<td data-header="注册类别">二级临时注册建造师</td>n<td data-header="注册号（执业印章号）">滇204090900437(临)</td>n<td data-header="注册专业">建筑工程</td>n</tr>n<tr>n<td data-header="序号">5</td>n<td data-header="姓名" style="font-size: 16px;">n<a href="javascript:void(0)" onclick="top.window.location.href="/dataservice/query/staff/staffDetail/001610081853024279"">杨继军</a>n</td>n<td data-header="身份证号">5329017******41</td>n<td data-header="注册类别">二级临时注册建造师</td>n<td data-header="注册号（执业印章号）">滇204080800079(临)</td>n<td data-header="注册专业">建筑工程</td>n</tr>n<tr>n<td data-header="序号">6</td>n<td data-header="姓名" style="font-size: 16px;">n<a href="javascript:void(0)" onclick="top.window.location.href="/dataservice/query/staff/staffDetail/001610081853017681"">王晓东</a>n</td>n<td data-header="身份证号">5329017******43</td>n<td data-header="注册类别">二级临时注册建造师</td>n<td data-header="注册号（执业印章号）">滇204080800076(临)</td>n<td data-header="注册专业">建筑工程</td>n</tr>n<tr>n<td data-header="序号">7</td>n<td data-header="姓名" style="font-size: 16px;">n<a href="javascript:void(0)" onclick="top.window.location.href="/dataservice/query/staff/staffDetail/001610081903290929"">马江伟</a>n</td>n<td data-header="身份证号">5329011972******14</td>n<td data-header="注册类别">一级临时注册建造师</td>n<td data-header="注册号（执业印章号）">云153000800777</td>n<td data-header="注册专业">建筑工程</td>n</tr>n<tr>n<td data-header="序号">8</td>n<td data-header="姓名" style="font-size: 16px;">n<a href="javascript:void(0)" onclick="top.window.location.href="/dataservice/query/staff/staffDetail/001610081857523624"">杨凤鸣</a>n</td>n<td data-header="身份证号">5329011955******35</td>n<td data-header="注册类别">一级临时注册建造师</td>n<td data-header="注册号（执业印章号）">云153000800779</td>n<td data-header="注册专业">建筑工程</td>n</tr>n<tr>n<td data-header="序号">9</td>n<td data-header="姓名" style="font-size: 16px;">n<a href="javascript:void(0)" onclick="top.window.location.href="/dataservice/query/staff/staffDetail/001610081852830307"">刘文敏</a>n</td>n<td data-header="身份证号">5329011973******28</td>n<td data-header="注册类别">二级注册建造师</td>n<td data-header="注册号（执业印章号）">滇229151637477</td>n<td data-header="注册专业">建筑工程</td>n</tr>n<tr>n<td data-header="序号">10</td>n<td data-header="姓名" style="font-size: 16px;">n<a href="javascript:void(0)" onclick="top.window.location.href="/dataservice/query/staff/staffDetail/001808040312139033"">李顺莲</a>n</td>n<td data-header="身份证号">5329011979******25</td>n<td data-header="注册类别">二级注册建造师</td>n<td data-header="注册号（执业印章号）">滇229121323131</td>n<td data-header="注册专业">建筑工程</td>n</tr>n<tr>n<td data-header="序号">11</td>n<td data-header="姓名" style="font-size: 16px;">n<a href="javascript:void(0)" onclick="top.window.location.href="/dataservice/query/staff/staffDetail/001807250313652527"">杨帝龙</a>n</td>n<td data-header="身份证号">5329011988******30</td>n<td data-header="注册类别">二级注册建造师</td>n<td data-header="注册号（执业印章号）">滇290171805314</td>n<td data-header="注册专业">建筑工程</td>n</tr>n<tr>n<td data-header="序号">12</td>n<td data-header="姓名" style="font-size: 16px;">n<a href="javascript:void(0)" onclick="top.window.location.href="/dataservice/query/staff/staffDetail/001610081901078436"">李利苟</a>n</td>n<td data-header="身份证号">5329011963******51</td>n<td data-header="注册类别">二级注册建造师</td>n<td data-header="注册号（执业印章号）">滇229111324636</td>n<td data-header="注册专业">建筑工程</td>n</tr>n<tr>n<td data-header="序号">13</td>n<td data-header="姓名" style="font-size: 16px;">n<a href="javascript:void(0)" onclick="top.window.location.href="/dataservice/query/staff/staffDetail/001610081852827519"">赵尚宏</a>n</td>n<td data-header="身份证号">5329011989******18</td>n<td data-header="注册类别">二级注册建造师</td>n<td data-header="注册号（执业印章号）">滇229131428456</td>n<td data-header="注册专业">建筑工程</td>n</tr>n<tr>n<td data-header="序号">14</td>n<td data-header="姓名" style="font-size: 16px;">n<a href="javascript:void(0)" onclick="top.window.location.href="/dataservice/query/staff/staffDetail/001809010349227049"">刘杰</a>n</td>n<td data-header="身份证号">5329011989******19</td>n<td data-header="注册类别">二级注册建造师</td>n<td data-header="注册号（执业印章号）">滇229121322755</td>n<td data-header="注册专业">建筑工程</td>n</tr>n<tr>n<td data-header="序号">15</td>n<td data-header="姓名" style="font-size: 16px;">n<a href="javascript:void(0)" onclick="top.window.location.href="/dataservice/query/staff/staffDetail/001905050413613792"">茶进泽</a>n</td>n<td data-header="身份证号">5329271995******71</td>n<td data-header="注册类别">二级注册建造师</td>n<td data-header="注册号（执业印章号）">滇229181900261</td>n<td data-header="注册专业">市政公用工程</td>n</tr>n<tr>n<td data-header="序号">16</td>n<td data-header="姓名" style="font-size: 16px;">n<a href="javascript:void(0)" onclick="top.window.location.href="/dataservice/query/staff/staffDetail/001905140342351236"">赵峰平</a>n</td>n<td data-header="身份证号">5329011980******35</td>n<td data-header="注册类别">二级注册建造师</td>n<td data-header="注册号（执业印章号）">滇229181900268</td>n<td data-header="注册专业">机电工程</td>n</tr>n<tr>n<td data-header="序号">17</td>n<td data-header="姓名" style="font-size: 16px;">n<a href="javascript:void(0)" onclick="top.window.location.href="/dataservice/query/staff/staffDetail/001905140342350580"">卢斌</a>n</td>n<td data-header="身份证号">5329011978******16</td>n<td data-header="注册类别">二级注册建造师</td>n<td data-header="注册号（执业印章号）">滇229181900269</td>n<td data-header="注册专业">建筑工程</td>n</tr>n<tr>n<td data-header="序号">18</td>n<td data-header="姓名" style="font-size: 16px;">n<a href="javascript:void(0)" onclick="top.window.location.href="/dataservice/query/staff/staffDetail/001704300250567681"">王明福</a>n</td>n<td data-header="身份证号">5323011983******3X</td>n<td data-header="注册类别">二级注册建造师</td>n<td data-header="注册号（执业印章号）">滇253071003485</td>n<td data-header="注册专业">市政公用工程</td>n</tr>n<tr>n<td data-header="序号">19</td>n<td data-header="姓名" style="font-size: 16px;">n<a href="javascript:void(0)" onclick="top.window.location.href="/dataservice/query/staff/staffDetail/001610081852859046"">沈惠君</a>n</td>n<td data-header="身份证号">5329011970******25</td>n<td data-header="注册类别">二级注册建造师</td>n<td data-header="注册号（执业印章号）">滇204070900576</td>n<td data-header="注册专业">建筑工程</td>n</tr>n<tr>n<td data-header="序号">20</td>n<td data-header="姓名" style="font-size: 16px;">n<a href="javascript:void(0)" onclick="top.window.location.href="/dataservice/query/staff/staffDetail/001703070250339224"">李锐民</a>n</td>n<td data-header="身份证号">5329011972******19</td>n<td data-header="注册类别">二级注册建造师</td>n<td data-header="注册号（执业印章号）">滇204070900048</td>n<td data-header="注册专业">建筑工程</td>n</tr>n<tr>n<td data-header="序号">21</td>n<td data-header="姓名" style="font-size: 16px;">n<a href="javascript:void(0)" onclick="top.window.location.href="/dataservice/query/staff/staffDetail/001610082226519583"">朱学斌</a>n</td>n<td data-header="身份证号">5329011972******93</td>n<td data-header="注册类别">二级注册建造师</td>n<td data-header="注册号（执业印章号）">滇204070900047</td>n<td data-header="注册专业">建筑工程</td>n</tr>n<tr>n<td data-header="序号">22</td>n<td data-header="姓名" style="font-size: 16px;">n<a href="javascript:void(0)" onclick="top.window.location.href="/dataservice/query/staff/staffDetail/001804030338847824"">王莲</a>n</td>n<td data-header="身份证号">5329011974******26</td>n<td data-header="注册类别">二级注册建造师</td>n<td data-header="注册号（执业印章号）">滇290171803652</td>n<td data-header="注册专业">市政公用工程</td>n</tr>n<tr>n<td data-header="序号">23</td>n<td data-header="姓名" style="font-size: 16px;">n<a href="javascript:void(0)" onclick="top.window.location.href="/dataservice/query/staff/staffDetail/001610081901072528"">张咏涛</a>n</td>n<td data-header="身份证号">5329011974******32</td>n<td data-header="注册类别">二级注册建造师</td>n<td data-header="注册号（执业印章号）">滇253081003487</td>n<td data-header="注册专业">建筑工程</td>n</tr>n<tr>n<td data-header="序号">24</td>n<td data-header="姓名" style="font-size: 16px;">n<a href="javascript:void(0)" onclick="top.window.location.href="/dataservice/query/staff/staffDetail/001610081901057862"">许建泉</a>n</td>n<td data-header="身份证号">5329011975******15</td>n<td data-header="注册类别">二级注册建造师</td>n<td data-header="注册号（执业印章号）">滇253081003486</td>n<td data-header="注册专业">建筑工程</td>n</tr>n<tr>n<td data-header="序号">25</td>n<td data-header="姓名" style="font-size: 16px;">n<a href="javascript:void(0)" onclick="top.window.location.href="/dataservice/query/staff/staffDetail/001804030338847697"">李卫东</a>n</td>n<td data-header="身份证号">5329011975******1X</td>n<td data-header="注册类别">二级注册建造师</td>n<td data-header="注册号（执业印章号）">滇290171803665</td>n<td data-header="注册专业">建筑工程</td>n</tr>n<script src="/assets/core/js/common/jquery/jquery-1.11.3.min.js" type="text/javascript"></script>n<script src="/assets/core/js/common/jquery/jquery.coo-kie.js" type="text/javascript"></script>n<script type="text/javascript">jQuery.noConflict();</script>n<script src="/asite/jsbpp/js/index.js" type="text/javascript"></script>n<tr>n<td colspan="6">n<div class="clearfix"><form action="/dataservice/query/comp/regStaffList/001607220057196741" class="pagingform" method="post" name="$pgfm"></form><script>__pgfm('',{"$total":37,"$reload":0,"$pg":1,"$pgsz":25})</script> <a sf="pagebar" sf:data="({pg:1,ps:25,tt:37,pn:5,pc:2,id:'',st:true})"></a></div>n<script src="/asite/jsbpp/js/jqGridPageDecorate.js" type="text/javascript"></script>n</td>n</tr>n</tbody>n</table>"}", "{"pg": 2, "trs": "<table class="pro_table_box pro_table_borderright" width="100%">n<colgroup>n<col width="5%"/>n<col width="15%"/>n<col width="20%"/>n<col width="20%"/>n<col width="20%"/>n<col width="20%"/>n</colgroup>n<thead>n<tr>n<th colspan="6" style=" background: #fff; text-align: left;">n<div class="comp_regstaff_links">n<a class="formsubmit selected" data-url="/dataservice/query/comp/regStaffList/001607220057196741/" href="javascript:void(0)">全部<span>（37）</span></a>rntttttrnttttt其中：rntttttrnttttt<a class="formsubmit" data-url="/dataservice/query/comp/regStaffList/001607220057196741/" href="javascript:void(0)" reg_type="RY_ZCLB_071">一级注册建造师<span>（6）</span></a>n<a class="formsubmit" data-url="/dataservice/query/comp/regStaffList/001607220057196741/" href="javascript:void(0)" reg_type="RY_ZCLB_072">二级注册建造师<span>（23）</span></a>n<a class="formsubmit" data-url="/dataservice/query/comp/regStaffList/001607220057196741/" href="javascript:void(0)" reg_type="RY_ZCLB_073">一级临时注册建造师<span>（2）</span></a>n<a class="formsubmit" data-url="/dataservice/query/comp/regStaffList/001607220057196741/" href="javascript:void(0)" reg_type="RY_ZCLB_074">二级临时注册建造师<span>（6）</span></a>n</div>n</th>n</tr>n<tr>n<th>序号</th>n<th>姓名</th>n<th>身份证号</th>n<th>注册类别</th>n<th>注册号（执业印章号）</th>n<th>注册专业</th>n</tr>n</thead>n<tbody>n<tr>n<td data-header="序号">26</td>n<td data-header="姓名" style="font-size: 16px;">n<a href="javascript:void(0)" onclick="top.window.location.href="/dataservice/query/staff/staffDetail/001610082226522354"">杨思武</a>n</td>n<td data-header="身份证号">5329011977******14</td>n<td data-header="注册类别">二级注册建造师</td>n<td data-header="注册号（执业印章号）">滇253081116758</td>n<td data-header="注册专业">建筑工程</td>n</tr>n<tr>n<td data-header="序号">27</td>n<td data-header="姓名" style="font-size: 16px;">n<a href="javascript:void(0)" onclick="top.window.location.href="/dataservice/query/staff/staffDetail/001610081852832404"">沈智中</a>n</td>n<td data-header="身份证号">5329011985******14</td>n<td data-header="注册类别">二级注册建造师</td>n<td data-header="注册号（执业印章号）">滇204141532338</td>n<td data-header="注册专业">市政公用工程</td>n</tr>n<tr>n<td data-header="序号">28</td>n<td data-header="姓名" style="font-size: 16px;">n<a href="javascript:void(0)" onclick="top.window.location.href="/dataservice/query/staff/staffDetail/001804030338848145"">张克</a>n</td>n<td data-header="身份证号">5329011989******12</td>n<td data-header="注册类别">二级注册建造师</td>n<td data-header="注册号（执业印章号）">滇290171803656</td>n<td data-header="注册专业">建筑工程</td>n</tr>n<tr>n<td data-header="序号">29</td>n<td data-header="姓名" style="font-size: 16px;">n<a href="javascript:void(0)" onclick="top.window.location.href="/dataservice/query/staff/staffDetail/001610082226522622"">杨凤军</a>n</td>n<td data-header="身份证号">5329291982******19</td>n<td data-header="注册类别">二级注册建造师</td>n<td data-header="注册号（执业印章号）">滇253071003488</td>n<td data-header="注册专业">建筑工程</td>n</tr>n<tr>n<td data-header="序号">30</td>n<td data-header="姓名" style="font-size: 16px;">n<a href="javascript:void(0)" onclick="top.window.location.href="/dataservice/query/staff/staffDetail/001804030338848229"">段一柱</a>n</td>n<td data-header="身份证号">5329321988******52</td>n<td data-header="注册类别">二级注册建造师</td>n<td data-header="注册号（执业印章号）">滇290171803643</td>n<td data-header="注册专业">建筑工程</td>n</tr>n<tr>n<td data-header="序号">31</td>n<td data-header="姓名" style="font-size: 16px;">n<a href="javascript:void(0)" onclick="top.window.location.href="/dataservice/query/staff/staffDetail/001610081901073510"">康建武</a>n</td>n<td data-header="身份证号">5332221983******16</td>n<td data-header="注册类别">二级注册建造师</td>n<td data-header="注册号（执业印章号）">滇253071003389</td>n<td data-header="注册专业">市政公用工程</td>n</tr>n<tr>n<td data-header="序号">32</td>n<td data-header="姓名" style="font-size: 16px;">n<a href="javascript:void(0)" onclick="top.window.location.href="/dataservice/query/staff/staffDetail/001610081856452565"">董建标</a>n</td>n<td data-header="身份证号">5329011971******10</td>n<td data-header="注册类别">一级注册建造师</td>n<td data-header="注册号（执业印章号）">云153070961918</td>n<td data-header="注册专业">建筑工程</td>n</tr>n<tr>n<td data-header="序号">33</td>n<td data-header="姓名" style="font-size: 16px;">n<a href="javascript:void(0)" onclick="top.window.location.href="/dataservice/query/staff/staffDetail/001610081856452181"">杜德胜</a>n</td>n<td data-header="身份证号">5329011969******1X</td>n<td data-header="注册类别">一级注册建造师</td>n<td data-header="注册号（执业印章号）">云153060961919</td>n<td data-header="注册专业">建筑工程</td>n</tr>n<tr>n<td data-header="序号">34</td>n<td data-header="姓名" style="font-size: 16px;">n<a href="javascript:void(0)" onclick="top.window.location.href="/dataservice/query/staff/staffDetail/001610081903260191"">杨卫超</a>n</td>n<td data-header="身份证号">5329011972******18</td>n<td data-header="注册类别">一级注册建造师</td>n<td data-header="注册号（执业印章号）">云153060961922</td>n<td data-header="注册专业">建筑工程</td>n</tr>n<tr>n<td data-header="序号">35</td>n<td data-header="姓名" style="font-size: 16px;">n<a href="javascript:void(0)" onclick="top.window.location.href="/dataservice/query/staff/staffDetail/001610081856460235"">张雄</a>n</td>n<td data-header="身份证号">5329011969******1X</td>n<td data-header="注册类别">一级注册建造师</td>n<td data-header="注册号（执业印章号）">云153060961923</td>n<td data-header="注册专业">建筑工程</td>n</tr>n<tr>n<td data-header="序号">36</td>n<td data-header="姓名" style="font-size: 16px;">n<a href="javascript:void(0)" onclick="top.window.location.href="/dataservice/query/staff/staffDetail/001610081903283167"">邹顺琴</a>n</td>n<td data-header="身份证号">5329011977******27</td>n<td data-header="注册类别">一级注册建造师</td>n<td data-header="注册号（执业印章号）">云153060961924</td>n<td data-header="注册专业">建筑工程</td>n</tr>n<tr>n<td data-header="序号">37</td>n<td data-header="姓名" style="font-size: 16px;">n<a href="javascript:void(0)" onclick="top.window.location.href="/dataservice/query/staff/staffDetail/001610081856460395"">赵山</a>n</td>n<td data-header="身份证号">5329011977******37</td>n<td data-header="注册类别">一级注册建造师</td>n<td data-header="注册号（执业印章号）">云153131572053</td>n<td data-header="注册专业">建筑工程</td>n</tr>n<script src="/assets/core/js/common/jquery/jquery-1.11.3.min.js" type="text/javascript"></script>n<script src="/assets/core/js/common/jquery/jquery.coo-kie.js" type="text/javascript"></script>n<script type="text/javascript">jQuery.noConflict();</script>n<script src="/asite/jsbpp/js/index.js" type="text/javascript"></script>n<tr>n<td colspan="6">n<div class="clearfix"><form action="/dataservice/query/comp/regStaffList/001607220057196741" class="pagingform" method="post" name="$pgfm"></form><script>__pgfm('',{"$total":37,"$reload":0,"$pg":2,"$pgsz":25})</script> <a sf="pagebar" sf:data="({pg:2,ps:25,tt:37,pn:5,pc:2,id:'',st:true})"></a></div>n<script src="/asite/jsbpp/js/jqGridPageDecorate.js" type="text/javascript"></script>n</td>n</tr>n</tbody>n</table>"}"]'],
    # # da = pd.DataFrame(data=data)
    # driver = webdriver.Chrome()
    # driver.get('https://www.baidu.com')
    # for d in data:
    #     df = f7(driver, d)
    #     print(df.values)
    #     print(df.columns, df.dtypes)
