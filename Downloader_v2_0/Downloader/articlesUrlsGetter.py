import re

import requests
from bs4 import BeautifulSoup

from Downloader.urlRequest import UrlRequest


class ArticlesUrlsGetter:
    """
    input an url of the book, it will store all articles urls of the book in the article_urls properties of stats
    """
    def __init__(self,stats):
        self.url_request=UrlRequest('gbk')
        self.stats = stats

    def get_articles_urls(self,book_url):
        html = self.url_request.get(book_url)
        soup = BeautifulSoup(html, 'html.parser')
        result = soup.find('div', attrs={'id': 'list'})
        pattern = r'<a href="%s(.*?)">' % self.stats.book.id
        urls = re.findall(pattern, str(result))
        for i in range(len(urls)):
            self.stats.articles_urls.append(book_url + urls[i])
        self.stats.sum_tasks = len(self.stats.articles_urls)