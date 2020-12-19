import unittest

from Downloader_v1_0.url_request import UrlRequest


class UrlRequestTest(unittest.TestCase):

    def setUp(self) -> None:
        self.url_request = UrlRequest('utf-8')

    def test_file_read(self):
        self.url_request.pretend_header('../sources/headers_content')
        print(self.url_request.header_paras)
        self.assertEqual(bool(self.url_request.header_paras), True)

    def test_request(self):
        html = self.url_request.get('https://m.biqooge.com/s.php')
        print(html)
        self.assertEqual(bool(html), True)

    def test_post(self):
        data = {'keyword': '牧神记', 't': '1'}
        html = self.url_request.post(data, 'https://m.biqooge.com/s.php')
        print(html)
        self.assertEqual(bool(html), True)


if __name__ == '__main__':
    unittest.main()