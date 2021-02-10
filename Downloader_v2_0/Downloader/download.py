import os

import gevent
from gevent import pool, monkey


monkey.patch_all(thread=False)

from Downloader.downloadarticle import DownloadArticle


class Download:
    def __init__(self, stats,article_handler):
        self.stats = stats
        self.directory_path = None
        self.article_handler = article_handler

    def mkdir(self,store_directory_path):
        self.directory_path = os.path.join(store_directory_path, self.stats.book.title)
        if os.path.exists(self.directory_path):
            return False
        else:
            os.mkdir(self.directory_path)
            return True

    def _make_article(self, article_url):
        DownloadArticle(article_url).run(self.directory_path, self.article_handler)

    def download(self,gevent_pool_num):
        Pool = pool.Pool(gevent_pool_num)
        gevent.joinall([Pool.spawn(self._make_article, i) for i in self.stats.articles_urls])



