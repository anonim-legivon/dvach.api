from posixpath import join as url_join

import requests
from addict import Dict
from simplejson import JSONDecodeError

from .helpers import *


class ApiSession:
    HEADERS = {
        'User-agent': 'Mozilla/5.0 (Windows NT 6.1; rv:52.0) '
                      'Gecko/20100101 Firefox/52.0'
    }

    def __init__(self, proxies=None, headers=None):
        self.session = requests.Session()
        self.session.headers.update(headers if headers else self.HEADERS)
        if proxies:
            self.session.proxies.update(proxies)

    def request(self, method='get', url=None, **kwargs):
        response = self.session.request(method=method, url=url, **kwargs)

        try:
            return Dict(response.json())
        except JSONDecodeError:
            return response

    def get(self, *args):
        """
        Get url
        :param args: args for request
        :return:
        """
        url = url_join(URL, *args)
        try:
            response = self.session.get(url=url)
        except Exception as e:
            print('Something goes wrong:', e)
            return None
        else:
            try:
                return Dict(response.json())
            except JSONDecodeError:
                return response

    def post(self, **kwargs):
        """
        Post url
        :param kwargs: kwargs for request
        :return: request response
        """
        url = url_join(URL, kwargs['url'])
        try:
            response = self.session.post(url=url, data=kwargs['data'], files=kwargs['files'])
        except Exception as e:
            print('Something goes wrong:', e)
            return None
        else:
            try:
                return Dict(response.json())
            except JSONDecodeError:
                return response

    def update_headers(self, headers):
        if headers:
            self.session.headers.clear()
            self.session.headers.update(headers if headers else self.HEADERS)

    def update_proxies(self, proxies):
        if proxies:
            self.session.proxies.clear()
            self.session.proxies.update(proxies)
