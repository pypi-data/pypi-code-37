import requests
import zipfile
import io
import re
from logging import getLogger
from lxml import html
from urllib.parse import urljoin
from jrdb import parser, schema
from jrdb.model import JRDBData


class JRDBClient():
    re_schema_type = re.compile(r'([A-Z]*?)([0-9]*?)\.txt')

    def __init__(self, auth):
        self.session = requests.Session()
        self.session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
        self.session.auth = auth
        self.logger = getLogger(__name__)

    def download(self, url):
        return self.session.get(url, stream=True)

    def fetch_page(self, url):
        return self.session.get(url)

    def fetch_latest_urls(self):
        url = 'http://www.jrdb.com/member/data/'
        res = self.fetch_page(url)
        page = html.fromstring(res.content)
        urls = [urljoin(url, x) for x in page.xpath('//a/@href') if x.endswith('zip')]
        self.logger.debug('Fetched urls. {}'.format(urls))
        return urls

    def fetch_all_urls(self, url):
        res = self.fetch_page(url)
        page = html.fromstring(res.content)
        urls = [urljoin(url, x) for x in page.xpath('//a/@href') if x.endswith('zip')]
        self.logger.debug('Fetched urls. {}'.format(urls))
        return urls

    def fetch_jrdbdata(self, url):
        res = self.session.get(url, stream=True)
        z = zipfile.ZipFile(io.BytesIO(res.content))

        ret = list()
        for filename in z.namelist():
            self.logger.debug('Parsing data. filename: {}'.format(filename))
            schema_type, yymmdd = self.re_schema_type.findall(filename)[0]
            schema_type = schema_type.lower()
            if not schema.has(schema_type):
                self.logger.warn('Does not support schema type. [{}]'.format(schema_type))
                continue

            with z.open(filename) as f:
                records = [parser.convert(raw, schema.get(schema_type))
                           for raw in f.read().split(b'\r\n') if raw]

            self.logger.debug('Success. filename: {} schema: {} records:{}'.format(
                filename, schema_type, len(records))
            )
            ret.append(JRDBData(filename, schema_type, yymmdd, records))

        return ret
