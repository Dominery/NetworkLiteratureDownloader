import os

import gevent
from gevent import pool, monkey


monkey.patch_all(thread=False)

from Downloader_v1_0.article import Article
from Downloader_v1_0.book import Book


class Download:
    def __init__(self, book_name, settings):
        self.book = Book(book_name, settings)
        self.article = Article
        self.settings = settings
        self.directory_path = None

    def search_related_book(self):
        self.book.get_book_info()

    def get_article_urls(self, index):
        self.book.make_choice(index)
        self.book.get_urls_article()
        self.settings.sum_tasks = len(self.book.article_urls)

    def mkdir(self, directory_path):
        self.directory_path = os.path.join(directory_path, self.book.book_url[1])
        if os.path.exists(self.directory_path):
            return False
        else:
            os.mkdir(self.directory_path)
            return True

    def make_article(self, article_url):
        article = self.article(article_url)
        article.get_title()
        article.get_content()
        article.write(self.directory_path, self.settings.completed_article)
        self.settings.process += 1

    def download(self):
        Pool = pool.Pool(5)
        gevent.joinall([Pool.spawn(self.make_article, i) for i in self.settings.article_urls])



