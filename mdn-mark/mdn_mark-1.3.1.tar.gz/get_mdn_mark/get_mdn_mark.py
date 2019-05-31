"""
request the mdn marks or labels from baidu.com, so.com, sogou.com
auth: chenzhongrun
mail: chenzhongrun@bonc.com
com: bonc
release data: 2019-0529
"""


import logging; logging.basicConfig(level=logging.INFO)
import time
import json
import csv
import sys
import os
import re
import getopt
from typing import Callable
from threading import Thread
from multiprocessing import Process

import requests_html
from zoran_tools.csv_tools import write_csv_row
from zoran_tools.path_tools import ask_file
from zoran_tools.zoran_tools import WithProgressBar
from zoran_tools.json_tools import jsonp_to_json
from zoran_tools.log import Logger

from .proxies import random_proxy, proxies


# constant val
SOURCES = {
    'baidu': {
        'name': '百度手机卫士',
        'url_pat': 'https://www.baidu.com/s?ie=UTF-8&wd={mdn}',
        'unsuccessful': ['采集失败', 'null', 'null', '百度手机卫士'],
    },
    '360': {
        'name': '360手机卫士',
        'url_pat': 'https://www.so.com/s?q={mdn}',
        'unsuccessful': ['采集失败', 'null', '360手机卫士'],
    },
    'sogou': {
        'name': '搜狗号码通',
        'url_pat': 'https://www.sogou.com/tx?query={mdn}',
        'unsuccessful': ['采集失败', '搜狗号码通'],
    },
    'sogou_api': {
        'name': '搜狗号码通',
        'url_pat': 'https://www.sogou.com/reventondc/inner/vrapi?number={mdn}&type=json&callback=show&isSogoDomain=1',
        'unsuccessful': ['采集失败', '搜狗号码通API'],
    }
}


# init val
start_time = time.strftime('%Y%m%d_%H%M%S')
failed = []
IPs = []


def generate_to_filename(from_filename: str, source: str='result') -> str:
    # generate a new file name for writing data by from file name
    prefix, suffix = os.path.splitext(from_filename)
    return '{prefix}.{source}.{time}{suffix}'.format(prefix=prefix, time=start_time, suffix=suffix, source=source)


def open_csv_utils(from_filename: str) -> list:
    # a utils function to open a csv file
    with open(from_filename, mode='r', encoding='utf8') as f:
        fr_csv = csv.reader(f)
        return list(fr_csv)


def down(url: str, proxies: bool=False, retry_times: int=3) -> (requests_html.HTMLResponse, bool):
    # request the url fro downloading response
    try:
        ss = requests_html.HTMLSession()
        if retry_times == 0:
            proxies = False
        if proxies:
            ss.proxies = random_proxy(ips=IPs)
            print(IPs)
        r = ss.get(url, timeout=3)
        if r.status_code == 200:
            return r, True
        if retry_times > 0:
            return down(url, proxies, retry_times-1)
        return None, False
    except BaseException:
        if retry_times:
            return down(url, proxies, retry_times-1)
        return None, False


def parse_baidu(r: requests_html.HTMLResponse) -> [str] * 4:
    # parse label from baidu.com
    label = r.html.xpath('//span[contains(@class, "op_fraudphone_label")]/text()')
    label = re.sub('\s', '', ''.join(label))
    cnt = r.html.xpath('//div[@class="op_fraudphone_word"]/text()')
    cnt = ''.join(cnt)
    cnt = re.findall('(\d+)', cnt)
    cnt = cnt[0] if cnt else '0'
    source = r.html.xpath('//div[@class="op_fraudphone_word"]/a/text()')
    source = re.sub('\s', '', ''.join(source))
    child = r.html.xpath('//div[@class="op_fraudphone_word"]/strong/text()')
    child = re.sub('"|\s', '', ''.join(child))

    if label:
        return [label, child, cnt, source]
    else:
        return ['未标记', '-', '0', '百度手机卫士']


def parse_360(r: requests_html.HTMLResponse) -> [str] * 3:
    # parse label from 360.com
    mark = r.html.xpath('//span[@class="mohe-ph-mark"]/text()')
    cnt = r.html.xpath('//span[./a[@class="mohe-sjws"]]/b/text()')
    mark = re.sub('\s', '', ''.join(mark))
    cnt = re.sub('\s', '', ''.join(cnt))
    if mark:
        return [mark, cnt, '306手机卫士']
    else:
        return ['未标记', '0', '306手机卫士']


def parse_sogou(r: requests_html.HTMLResponse) -> [str] * 2:
    # parse label from sogou.com
    label = re.findall('号码通用户数据：(.*)：', r.html.text)
    label = re.sub('\s', '', ''.join(label))
    if label:
        return [label, '搜狗号码通']
    else:
        return ['未标记', '搜狗号码通']


def parse_sogou_api(r: requests_html.HTMLResponse) -> [str] * 2:
    s = jsonp_to_json(r.html.text)
    try:
        j: dict = json.loads(s)
        info = j.get('NumInfo')
        mark = re.match('^号码通用户数据：(.*)：.*', info)
        if mark:
            mark = mark.groups()[0]
            return [mark, '搜狗号码通API']
        else:
            return ['未标记', '搜狗号码通API']
    except Exception:
        return ['采集失败', '搜狗号码通']


def crawl_from(mdn: str, parser: Callable[[requests_html.HTMLResponse], list],
               source: dict, proxies: bool=False) -> [str]:
    # to download and parse info from some platform
    url = source.get('url_pat').format(mdn=mdn)
    r, ok = down(url, proxies=proxies)
    if ok:
        return parser(r)
    else:
        return source.get('unsuccessful')


def crawl_from_baidu(mdn: str) -> [str]:
    # a shortcut for crawling from baidu
    return crawl_from(mdn=mdn, parser=parse_baidu, source=SOURCES.get('baidu'))


def crawl_from_360(mdn: str) -> [str]:
    # a shortcut for crawling from 360
    return crawl_from(mdn=mdn, parser=parse_360, source=SOURCES.get('360'))


def crawl_from_sogou(mdn: str) -> [str]:
    # a shortcut for crawling from sogou
    return crawl_from(mdn=mdn, parser=parse_sogou, source=SOURCES.get('sogou'), proxies=True)


def crawl_from_sogou_api(mdn: str) -> [str]:
    # a shortcut for crawling from sogou
    return crawl_from(mdn=mdn, parser=parse_sogou_api, source=SOURCES.get('sogou_api'), proxies=True)


def crawl_task(from_file: str, crawling_rows: list, source: str, crawler: Callable[[str], list]):
    # a task for threading to crawl from some source
    to_file = generate_to_filename(from_file, source)
    logger = Logger(source)
    logger.time(). \
        info('it is going to get mark from {source}. The results will be writen in {file}'.
             format(source=source, file=to_file))

    for row in WithProgressBar(crawling_rows):
        mdn = row[0]
        res = crawler(mdn)
        write_csv_row(to_file, row + res)

    logger.time().info('the task over. The results was writen in {}'.format(to_file))


def main():
    # with single threading
    logging.info('请求打开CSV文件')
    from_file = ask_file()
    to_file = generate_to_filename(from_file)
    logging.info('正在读取文件')
    rows = open_csv_utils(from_file)
    # print(rows)
    logging.info('{} 开始在百度，360手机出卫士，搜狗号码通查找号码标注，查找结果会写入:\n\t{}'.format(
        time.strftime('%Y-%m-%d %H:%M:%S'), to_file))
    for row in WithProgressBar(rows):
        mdn = row[0]
        res_baidu = crawl_from_baidu(mdn=mdn)
        res_360 = crawl_from_360(mdn=mdn)
        # res_sogou = crawl_from_sogou(mdn=mdn)
        # res_sogou_api = crawl_from_sogou_api(mdn=mdn)
        # write_csv_row(to_file, row=row + res_baidu + res_360 + res_sogou + res_sogou_api)
        write_csv_row(to_file, row=row + res_baidu + res_360 + ['未采集', '搜狗号码通'])
        # write_csv_rows(to_file, rows=[row + res_baidu, row + res_360, row + res_sogou])
    logging.info('查找结束，结果已写入{}'.format(to_file))
    logging.info(time.strftime('%Y-%m-%d %H:%M:%S'))


def threading_main(argv=sys.argv[1:]):
    # with multi threading
    # print(argv)
    ip_file = None
    if isinstance(argv, (list,tuple)) and '-i' in argv:
        print('请打开一个IP文件')
        ip_file = ask_file()
        if not ip_file:
            sys.exit(1)
    global IPs
    IPs = proxies(ip_file)

    logging.info('please open the nums csv file')
    from_file = ask_file()
    logging.info('it is reading the file')
    rows = open_csv_utils(from_file)
    # multi processing or multi threading ?
    task_baidu = Thread(target=crawl_task, args=(from_file, rows, 'baidu', crawl_from_baidu))
    task_360 = Thread(target=crawl_task, args=(from_file, rows, '360', crawl_from_360))
    task_sogou = Thread(target=crawl_task, args=(from_file, rows, 'sogou', crawl_from_sogou))
    task_sogou_api = Thread(target=crawl_task, args=(from_file, rows, 'sogou_api', crawl_from_sogou_api))
    # task_baidu = Process(target=crawl_task, args=(from_file, rows, 'baidu', crawl_from_baidu))
    # task_360 = Process(target=crawl_task, args=(from_file, rows, '360', crawl_from_360))
    # task_sogou = Process(target=crawl_task, args=(from_file, rows, 'sogou', crawl_from_sogou))
    # task_sogou_api = Process(target=crawl_task, args=(from_file, rows, 'sogou_api', crawl_from_sogou_api))
    for task in [task_baidu, task_360, task_sogou, task_sogou_api]:
        task.start()
    for task in [task_baidu, task_360, task_sogou, task_sogou_api]:
        task.join()


if __name__ == '__main__':
    # main()
    threading_main(sys.argv[1:])
