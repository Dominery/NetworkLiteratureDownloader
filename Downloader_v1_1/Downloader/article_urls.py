import re

from bs4 import BeautifulSoup

from Downloader.url_request import UrlRequest


class GetArticles:
    """
    input an url of the book, it will store all articles urls of the book in the article_urls properties of stats
    """
    def __init__(self,book_url,stats):
        self.url_request=UrlRequest('gbk')
        self.book_url = book_url
        self.stats = stats

    def get_articles_urls(self):
        html = self.url_request.get(self.book_url)
        soup = BeautifulSoup(html, 'html.parser')
        result = soup.find('div', attrs={'id': 'list'})
        pattern = r'<a href="%s(.*?)">' % (self.book_url[0])
        urls = re.findall(pattern, str(result))
        for i in range(len(urls)):
            self.stats.articles_urls.append(self.book_url + urls[i])
        self.stats.sum_tasks = len(self.stats.articles_urls)