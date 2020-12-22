import requests


class UrlRequest:
    header_paras = {}

    def __init__(self, encoding=None):
        self.encoding = encoding

    @classmethod
    def pretend_header(cls, header_paras_file):
        if cls.header_paras:
            with open(header_paras_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip('\n').replace(' ', '')
                    line_lst = line.split(':')
                    if len(line_lst) == 2:
                        cls.header_paras[line_lst[0]] = line_lst[1]
                    elif len(line_lst) > 2:
                        value = ''
                        for i in range(1, len(line_lst)):
                            value += line_lst[i]
                        cls.header_paras[line_lst[0]] = value
                    else:
                        raise ValueError('File Not Have Right Syntax!')

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
