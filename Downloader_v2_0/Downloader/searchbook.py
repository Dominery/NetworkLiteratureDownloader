import re
from collections import namedtuple
from bs4 import BeautifulSoup

from Downloader.urlRequest import UrlRequest


class SearchBook:
    """
    only search the books info which match the keyword user typed,and store the info as a namedtuple in stats
    """
    def __init__(self, search_book, settings):
        self.settings = settings
        self.search_url = settings.search_url
        self.book_name = search_book
        UrlRequest.pretend_header(self.settings.request_head_paras_file)
        self.url_request = UrlRequest('utf-8')

    def get_book_info(self,books_urls):
        data = {'keyword': self.book_name, 't': '1'}
        html = self.url_request.post(data, self.search_url)
        self._parse_book_html(html,books_urls)

    def _parse_book_html(self, html, books_urls):
        soup = BeautifulSoup(html, 'html.parser')
        books = soup.find_all('div', attrs={'class': 'hot_sale'})
        for book in books:
            books_urls.append(self._set_book(str(book)))

    def _set_book(self,html):
        Book = namedtuple('Book', ['id', 'title', 'author'])
        book_id = re.search(r'<a href="(/.*?/)">', html)
        title = re.search(r'<p class="title">(.*?)</p>', html)
        author = re.search(r'<p class="author">.*作者：(.*?)</p>', html)
        return Book(book_id[1], title[1], author[1])

