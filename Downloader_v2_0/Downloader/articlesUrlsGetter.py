import re

import requests
from bs4 import BeautifulSoup

from Downloader.urlRequest import UrlRequest


class ArticlesUrlsGetter:
    """
    input an url of the book, it will store all articles urls of the book in the article_urls properties of stats
    """
    def __init__(self):
        self.url_request=UrlRequest('gbk')

    def get_articles_urls(self,index_url,book_id):
        book_url = index_url + book_id
        html = self.url_request.get(book_url)
        soup = BeautifulSoup(html, 'html.parser')
        result = soup.find('div', attrs={'id': 'list'})
        pattern = r'<a href="%s(.*?)">' % book_id
        urls = re.findall(pattern, str(result))
        articles_urls = []
        for i in range(len(urls)):
            articles_urls.append(book_url + urls[i])
        return articles_urls
