# -*- coding: utf-8 -*-

import json
import logging

import curlify
from requests import Session


logger = logging.getLogger(__name__)


class RemoteApiSession(Session):
    __attrs__ = Session.__attrs__ + ['_base_url', '_prefix']

    def __init__(self, base_url: str, *, prefix: str = None):
        super().__init__()

        self._base_url = base_url
        self._prefix = prefix

    def __repr__(self):
        return f'{self.__class__.__name__}({self.url})'

    @property
    def base_url(self):
        return self._base_url

    @property
    def prefix(self):
        return self._prefix

    @property
    def url(self):
        return self._build_url(self._base_url, self._prefix)

    def request(self, method: str, url_path: str, **kwargs):

        url = self._build_url(self.url, url_path)

        logger.info(
            f'Performing "{method}" request to "{url}"'
            f'\nRequest params: {self._serialize(kwargs)}')

        resp = super().request(method, url, **kwargs)

        try:
            resp_content = self._serialize(resp.json())
        except ValueError:
            resp_content = resp.text

        logger.info(
            f'{curlify.to_curl(resp.request)}'
            f'\nResponse status code is "{resp.status_code}"'
            f'\n{resp_content}'
            f'\nHeaders: {self._serialize(dict(resp.headers))}'
            f'\nResponse time is "{resp.elapsed.total_seconds()}" seconds')

        return resp

    @staticmethod
    def _build_url(base, path: str):
        return base.rstrip('/') + '/' + path.lstrip('/') if path else base

    @staticmethod
    def _serialize(obj):
        return json.dumps(
            obj, ensure_ascii=False, indent=4,
            default=lambda o: repr(o))
