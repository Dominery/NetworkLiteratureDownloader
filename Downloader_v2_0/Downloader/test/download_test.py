import unittest

from Downloader_v1_1_0.download import Download
from Downloader_v1_1_0.settings import Settings


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        settings = Settings()
        settings.request_head_paras_file = '../sources/headers_content'
        self.download = Download('牧神记',settings)

    def test_make_article(self):
        self.download.directory_path = './'
        self.download._make_article('https://www.biqooge.com/4_4074/13632514.html')
        self.assertEqual(self.download.stats.process, 1)

    def test_download(self):
        self.download.directory_path = './'
        self.download.stats.process =0
        self.download.stats.article_urls = ['https://www.biqooge.com/0_1/33252800.html', 'https://www.biqooge.com/0_1/33257756.html']
        self.download.download()
        self.assertEqual(self.download.stats.process, 2)


if __name__ == '__main__':
    unittest.main()
