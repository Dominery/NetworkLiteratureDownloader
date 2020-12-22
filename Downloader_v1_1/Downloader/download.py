import os

import gevent
from gevent import pool, monkey


monkey.patch_all(thread=False)

from Downloader.downloadarticle import DownloadArticle


class Download:
    def __init__(self, stats,settings):
        self.article = DownloadArticle
        self.stats = stats
        self.settings = settings
        self.directory_path = None

    def mkdir(self):
        self.directory_path = os.path.join(self.settings.store_directory_path, self.stats.book.title)
        if os.path.exists(self.directory_path):
            return False
        else:
            os.mkdir(self.directory_path)
            return True

    def _make_article(self, article_url):
        article = self.article(article_url)
        try:
            article.get_title()
            article.get_content()
            article.write(self.directory_path, self.stats.completed_article)
        except Exception:
            pass
        self.stats.process += 1

    def download(self):
        Pool = pool.Pool(self.settings.gevent_pool_num)
        gevent.joinall([Pool.spawn(self._make_article, i) for i in self.stats.article_urls])



