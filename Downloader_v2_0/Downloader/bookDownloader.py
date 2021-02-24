import os

import gevent
from gevent import pool, monkey

from Downloader.articleTitleFormatter import ArticleTitleFormatter
from Downloader.txtExporter import TextExporter

monkey.patch_all(thread=False)

from Downloader.articleparser import ArticleParser


class BookDownloader:
    def __init__(self, stats,article_handler):
        self.stats = stats
        self.directory_path = None
        self.article_handler = article_handler
        self.exporter = TextExporter()
        self.article_title_formatter = ArticleTitleFormatter(len(str(self.stats.sum_tasks)))

    def mkdir(self,store_directory_path):
        self.directory_path = os.path.join(store_directory_path, self.stats.book.title)
        if not os.path.exists(self.directory_path):
            os.mkdir(self.directory_path)

    def _make_article(self, article_url):
        title = ""
        try:
            article = ArticleParser(article_url).parse(self.article_title_formatter)
            title = article.title
        except Exception as e:
            print(e)
        else:
            self.exporter.export(article,self.directory_path)
        finally:
            self.article_handler(title)

    def download(self,gevent_pool_num):
        Pool = pool.Pool(gevent_pool_num)
        gevent.joinall([Pool.spawn(self._make_article, i) for i in self.stats.articles_urls])



