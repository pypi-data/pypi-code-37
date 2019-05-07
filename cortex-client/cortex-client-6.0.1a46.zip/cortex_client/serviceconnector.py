"""
Copyright 2018 Cognitive Scale, Inc. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from typing import Dict

import requests


class ServiceConnector:
    """
    Defines the settings and security credentials required to access a service.
    """
    def __init__(self, url, version, token, verify_ssl_cert=True):
        self.url = url
        self.version = version
        self.token = token
        self.verify_ssl_cert = verify_ssl_cert

    ## properties ##

    @property
    def base_url(self):
        return u'{0}/v{1}'.format(self.url, self.version)

    ## methods ##

    def post_file(self, uri, files, data, headers=None):
        """
        Posts to a service, extending the path with the specified uri.

        :param uri: path to extend service url
        :param files: files to send to the service
        :param data: data to send as the post body to the service
        :param headers: HTTP headers for the post
        """
        headersToSend = self._construct_headers(headers)
        url = self._construct_url(uri)
        return requests.post(url, files=files, data=data, headers=headersToSend,
                             verify=self.verify_ssl_cert)

    def request(self, method, uri, body=None, headers=None, **kwargs):
        """
        Sends a request to the specified uri.

        :param method: HTTP method to send to the service
        :param uri: path to extend service url
        :param data: data to send as the post body to the service
        :param headers: HTTP headers for this post
        :param kwargs: additional key-value pairs to pass to the request method
        :return: :class:`Response <Response>` object
        """
        headersToSend = self._construct_headers(headers)
        url = self._construct_url(uri)
        return requests.request(
            method,
            url,
            data=body,
            headers=headersToSend,
            verify=self.verify_ssl_cert,
            **kwargs
        )

    @staticmethod
    def urljoin(pieces):
        """
        Joins together the pieces of a URL.

        :parma pieces: strings representing the pieces of a URL
        :return: a string representing the joined pieces of the URL
        """
        pieces = [_f for _f in [s.rstrip('/') for s in pieces] if _f]
        return '/'.join(pieces)

    ## private ##

    def _construct_url(self, uri):
        return self.urljoin([self.base_url, uri])

    def _construct_headers(self, headers):
        headersToSend = {}

        if self.token:
            auth = 'Bearer {}'.format(self.token)
            headersToSend[u'Authorization'] = auth

        if headers is not None:
            headersToSend.update(headers)
        return headersToSend
