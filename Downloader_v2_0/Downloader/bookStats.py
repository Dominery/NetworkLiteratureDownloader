from Downloader.articlesUrlsGetter import ArticlesUrlsGetter
from Downloader.bookInfoSearcher import BookInfoSearcher


class BookStats:
    """
    using Facade pattern to make the BookStats Class manage the complicated ports of child classes
    the effect of this class is to found the info and store for one book
    """
    def __init__(self,book,settings):
        self.settings = settings
        self.articles_urls = []
        self.sum_tasks = 0
        self.book = book
        self.book_url = None
        self._books_infos = []

    def search(self):
        if isinstance(self.book,str):
            self._books_infos = BookInfoSearcher().get_book_info(self.book,self.settings.search_url)

    def get_article(self):
        if isinstance(self.book,tuple):
            book_url = self.settings.index_url + self.book[0]
            ArticlesUrlsGetter(self).get_articles_urls(book_url)

    @property
    def books_infos(self):
        return tuple(book for book in self._books_infos)

    def __eq__(self, other):
        return self.book == other.book


