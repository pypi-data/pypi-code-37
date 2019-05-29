"""
request the mdn marks or labels from baidu.com, so.com, sogou.com
auth: chenzhongrun
mail: chenzhongrun@bonc.com
com: bonc
release data: 2019-0529
"""


import logging; logging.basicConfig(level=logging.INFO)
import time
import csv
import os
import re
from typing import Callable

import requests_html
from zoran_tools.csv_tools import write_csv_row
from zoran_tools.path_tools import ask_file
from zoran_tools.zoran_tools import WithProgressBar


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
        'unsuccessful': ['采集失败', 'null', '搜狗号码通'],
    }
}


# init val
start_time = time.strftime('%Y%m%d_%H%M%S')


def generate_to_filename(from_filename: str) -> str:
    # generate a new file name for writing data by from file name
    prefix, suffix = os.path.splitext(from_filename)
    return '{prefix}.result.{time}{suffix}'.format(prefix=prefix, time=start_time, suffix=suffix)


def open_csv_utils(from_filename: str) -> list:
    # a utils function to open a csv file
    with open(from_filename, mode='r', encoding='utf8') as f:
        fr_csv = csv.reader(f)
        return list(fr_csv)


def down(url: str) -> (requests_html.HTMLResponse, bool):
    # request the url fro downloading response
    try:
        r = requests_html.HTMLSession().get(url)
        if r.status_code == 200:
            # r.html.render()
            return r, True
        else:
            return None, False
    except BaseException:
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


def crawl_from(mdn: str, parser: Callable[[requests_html.HTMLResponse], list], source: dict) -> [str]:
    # to download and parse info from some platform
    url = source.get('url_pat').format(mdn=mdn)
    r, ok = down(url)
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
    return crawl_from(mdn=mdn, parser=parse_sogou, source=SOURCES.get('sogou'))


def main():
    logging.info('请求打开CSV文件')
    from_file = ask_file()
    to_file = generate_to_filename(from_file)
    logging.info('正在读取文件')
    rows = open_csv_utils(from_file)
    # print(rows)
    logging.info('开始在百度手机卫士/泰迪熊，360手机出卫士，搜狗号码通查找号码标注，查找结果会写入{}'.format(to_file))
    for row in WithProgressBar(rows):
        mdn = row[0]
        res_baidu = crawl_from_baidu(mdn=mdn)
        res_360 = crawl_from_360(mdn=mdn)
        res_sogou = crawl_from_sogou(mdn=mdn)
        write_csv_row(to_file, row=row + res_baidu + res_360 + res_sogou)
        # write_csv_rows(to_file, rows=[row + res_baidu, row + res_360, row + res_sogou])
    logging.info('查找结束，结果已写入{}'.format(to_file))


if __name__ == '__main__':
    main()
