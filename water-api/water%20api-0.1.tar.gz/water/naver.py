import os
from datetime import datetime
from urllib.parse import parse_qs, urlencode, urlparse, quote

import requests

from lxml import html

base_url = ""

headers = {"X-Naver-Client-Id": os.getenv('X_Naver_Client_Id'),
           "X-Naver-Client-Secret": os.getenv('X_Naver_Client_Secret')}


def get_query_field(url, field):
    try:
        return parse_qs(urlparse(url).query)[field]
    except KeyError:
        return []


def search(category='blog', query='hello'):
    query_dict = dict(query=query, display=100)
    url = "https://openapi.naver.com/v1/search/%(category)s?%(query)s" % dict(category=category, query=urlencode(query_dict))

    resp = requests.get(url, allow_redirects=True, headers=headers)
    print(resp.json())


def cafe(clubid=10050146, userDisplay=50):
    query_dict = {
        "search.boardtype": "L",
        "search.specialmenutype": "",
        "search.questionTab": "A",
        "search.totalCount": 401,
        "search.page": 1,
    }

    query_dict['search.clubid'] = clubid
    query_dict['userDisplay'] = userDisplay

    url = "http://cafe.naver.com/ArticleList.nhn?%s" % urlencode(query_dict)

    rst = []
    page = requests.get(url, allow_redirects=True)
    tree = html.fromstring(page.content.decode('cp949', 'ignore'))

    now = datetime.now()

    for article in tree.xpath("//div[(contains(@class,'article-board m-tcol-c')) and not(contains(@id, 'upperArticleList'))]/table/tbody/tr"):
        category = article.xpath("td[contains(@class, 'td_article')]/div[contains(@class, 'board-name')]/div/a")[0].text.strip()
        title = article.xpath("td[contains(@class, 'td_article')]/div[contains(@class, 'board-list')]/div/a")[0].text.strip()
        id = get_query_field(article.xpath("td[contains(@class, 'td_article')]/div[contains(@class, 'board-list')]/div/a/@href")[0], 'articleid')[0]
        username = article.xpath("td[contains(@class, 'td_name')]/div/table/tr/td/a")[0].text
        date = article.xpath("td[contains(@class, 'td_date')]")[0].text.split(":")

        ele = dict(
            id=id,
            title=title,
            category=category,
            username=username,
            created_at=now.replace(hour=int(date[0]), minute=int(date[1])).strftime("%Y-%m-%d %H:%M:%S")
        )
        rst.append(ele)

    return rst
