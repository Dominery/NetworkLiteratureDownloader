import re
from collections import namedtuple

from bs4 import BeautifulSoup

from Downloader.articleTitleFormatter import ArticleTitleFormatter
from Downloader.urlRequest import UrlRequest

Article = namedtuple("Article", ["title", "content"])


class ArticleParser:
    def __init__(self, article_url):
        self.url_request = UrlRequest('gbk')
        self.html = self.url_request.get(article_url)

    def _get_content(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        if soup:
            return soup.find('div', attrs={'id': 'content'}).text
        else:
            return ""

    def _get_title(self,formatter):
        raw_title = re.search(r'<h1>(.*?)</h1>', self.html)
        if raw_title:
            return formatter.format(raw_title[1])

    def parse(self):
        return Article(self._get_title(ArticleTitleFormatter()),self._get_content())
