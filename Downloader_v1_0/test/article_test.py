import unittest

from Downloader_v1_0.article import Article


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.article = Article('https://www.biqooge.com/4_4074/2912829.html')

    def test_get_content(self):
        self.article.get_content()
        self.assertEqual(bool(self.article.content),True)
        print(self.article.content)


if __name__ == '__main__':
    unittest.main()
