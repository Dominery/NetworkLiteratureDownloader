import os

import requests
import json


class UrlRequest:
    header_paras = {}

    def __init__(self, encoding=None):
        self.encoding = encoding

    @classmethod
    def pretend_header(cls, header_paras_file):
        if not cls.header_paras and os.path.exists(header_paras_file):
            with open(header_paras_file, 'r') as f:
                cls.header_paras = json.load(f)

    def get(self, url):
        try:
            req = requests.get(url, timeout=30, headers=self.header_paras)
            req.raise_for_status()
            req.encoding = req.apparent_encoding if not self.encoding else self.encoding
            return req.text
        except Exception as e:
            print(e)
            return False

    def post(self, data, url):
        if not isinstance(data, dict):
            raise ValueError('ValueError: dict type was expected')
        session = requests.Session()
        session_json = session.post(url=url, headers=self.header_paras, data=data)
        session_json.encoding = self.encoding if self.encoding else session_json.apparent_encoding
        return session_json.text
