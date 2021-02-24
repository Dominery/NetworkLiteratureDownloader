import re
from collections import namedtuple
from bs4 import BeautifulSoup

from Downloader.settings import Settings
from Downloader.urlRequest import UrlRequest


class BookInfoSearcher:
    """
    only search the books info which match the keyword user typed,and store the info as a namedtuple in stats
    """
    def __init__(self):
        UrlRequest.pretend_header(Settings().request_head_paras_file)
        self.url_request = UrlRequest('utf-8')

    def get_book_info(self,book_name,search_url):
        data = {'keyword': book_name, 't': '1'}
        html = self.url_request.post(data, search_url)
        return self._parse_book_html(html)

    def _parse_book_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        books = soup.find_all('div', attrs={'class': 'hot_sale'})
        books_urls = []
        for book in books:
            books_urls.append(self._set_book(str(book)))
        return books_urls

    def _set_book(self,html):
        Book = namedtuple('Book', ['id', 'title', 'author'])
        book_id = re.search(r'<a href="(/.*?/)">', html)
        title = re.search(r'<p class="title">(.*?)</p>', html)
        author = re.search(r'<p class="author">.*作者：(.*?)</p>', html)
        return Book(book_id[1], title[1], author[1])

