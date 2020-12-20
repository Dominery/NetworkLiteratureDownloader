import unittest
from collections import namedtuple
from unittest import mock

from Downloader_v1_0.book import Book


class BookTest(unittest.TestCase):
    def setUp(self) -> None:
        self.book = Book('1')

    def test_get_book_info(self):
        with open('text_book_html','r',encoding='utf-8')as f:
            html_str = f.read()
        self.book.parse_book_html(html_str)
        self.assertEqual(bool(self.book.book_url), True)

    def user_make_choice(self,prompt):
        if 'choose' in prompt.lower():
            return 0

    def test_make_choice(self):
        s = namedtuple('Book', ['id', 'title', 'author'])
        self.book.book_url = [s('/4_4074/','牧神记','宅猪')]
        with mock.patch('builtins.input',new=self.user_make_choice):
            self.book.make_choice()
            self.assertIsInstance(self.book.book_url,tuple)
            print(self.book.book_url)

    def test_get_urls_article(self):
        s = namedtuple('Book', ['id', 'title', 'author'])
        self.book.book_url = s('/4_4074/','牧神记','宅猪')
        self.book.get_urls_article()
        self.assertEqual(bool(self.book.article_url),True)
        print(self.book.article_url[0:6])



if __name__ == '__main__':
    unittest.main()
