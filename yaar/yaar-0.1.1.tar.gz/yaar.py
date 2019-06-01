# -*- coding: utf-8 -*-
"""This module implements a simple asynchronous interface for
http requests.

Usage:
``````

.. code-block:: python

    import yaar
    response = await yaar.get('http://google.com/')
    print(response.text)
"""

# Copyright 2019 Juca Crispim <juca@poraodojuca.net>

# This file is part of yaar.

# yaar is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# yaar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with yaar. If not, see <http://www.gnu.org/licenses/>.

import asyncio
import json
import aiohttp


class BadHTTPRequest(Exception):
    pass


class Response:
    """Encapsulates a response from a http request"""

    def __init__(self, status, text):
        """Constructor for Response.

        :param status: The response status.
        :param text: The response text."""
        self.status = status
        self.text = text

    def json(self):
        """Loads the json in the response text."""

        return json.loads(self.text)


async def _request(method, url, **kwargs):
    """Performs a http request and returns an instance of
    :class:`yaar.core.requests.Response`

    :param method: The requrest's method.
    :param url: Request's url.
    :param kwargs: Arguments passed to aiohttp.ClientSession.request
        method.
    """

    loop = asyncio.get_event_loop()

    client = aiohttp.ClientSession(loop=loop)
    try:
        resp = await client.request(method, url, **kwargs)
        status = resp.status
        text = await resp.text()
        await resp.release()
    finally:
        await client.close()

    r = Response(status, text)
    if r.status != 200:
        raise BadHTTPRequest(r.status, r.text)
    return r


async def get(url, **kwargs):
    """Performs a http GET request

    :param url: Request's url.
    :param kwargs: Args passed to :func:`yaar.core.requests._request`.
    """

    method = 'GET'
    resp = await _request(method, url, **kwargs)
    return resp


async def post(url, **kwargs):
    """Performs a http POST request

    :param url: Request's url.
    :param kwargs: Args passed to :func:`yaar.core.requests._request`.
    """

    method = 'POST'
    resp = await _request(method, url, **kwargs)
    return resp


async def put(url, **kwargs):
    """Performs a http PUT request

    :param url: Request's url.
    :param kwargs: Args passed to :func:`yaar.core.requests._request`.
    """

    method = 'PUT'
    resp = await _request(method, url, **kwargs)
    return resp


async def delete(url, **kwargs):
    """Performs a http DELETE request

    :param url: Request's url.
    :param kwargs: Args passed to :func:`yaar.core.requests._request`.
    """

    method = 'DELETE'
    resp = await _request(method, url, **kwargs)
    return resp
