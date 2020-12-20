import os
import time

import gevent
from gevent import pool,monkey
monkey.patch_all()

from Downloader_v1_0.article import Article
from Downloader_v1_0.book import Book


class Download:
    def __init__(self, book_name):
        self.book = Book(book_name)
        self.article = Article
        self.process = 0

    def get_article_urls(self):
        self.book.get_book_info()
        self.book.make_choice()
        self.book.get_urls_article()
        self.sum_threads = len(self.book.article_urls)

    def mkdir(self, directory_path):
        self.directory_path = os.path.join(directory_path, self.book.book_url[1])
        if os.path.exists(self.directory_path):
            return
        else:
            os.mkdir(self.directory_path)

    def make_article(self, article_url):
        article = self.article(article_url)
        article.get_title()
        article.get_content()
        article.write(self.directory_path)
        self.process += 1
        format_process = '\r[{:<20}]已下载:{:.2f}%'.format('#' * (self.process * 20 // self.sum_threads),
                                                        self.process / self.sum_threads*100)
        print(format_process, end='')

    def download(self, directory_path):
        start_time = time.time()
        self.get_article_urls()
        self.mkdir(directory_path)
        Pool = pool.Pool(5)
        gevent.joinall([Pool.spawn(self.make_article,i) for i in self.book.article_urls])
        end_time = time.time()
        print(f'\n共计耗时{end_time-start_time}')


def main():
    down = Download('牧神记')
    down.download('./')


if __name__ == '__main__':
    main()
