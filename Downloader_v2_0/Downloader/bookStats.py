from Downloader.articlesUrlsGetter import ArticlesUrlsGetter
from Downloader.bookInfoSearcher import BookInfoSearcher


class BookStats:
    """
    using Facade pattern to make the BookStats Class manage the complicated ports of child classes
    the effect of this class is to found the info and store for one book
    """
    def __init__(self,settings):
        self.settings = settings
        self.articles_urls = []
        self.sum_tasks = 0
        self._book = None
        self.book_url = None
        self._books_infos = []

    def search(self,book_name):
        self._books_infos = BookInfoSearcher().get_book_info(book_name,self.settings.search_url)

    def get_article(self):
        self.articles_urls = ArticlesUrlsGetter().get_articles_urls(self.settings.index_url, self._book.id)
        self.sum_tasks = len(self.articles_urls)

    def get_book_name(self):
        return self._book.title

    def choose_book(self,selected):
        self._book = self._books_infos[selected]

    @property
    def books_infos(self):
        return tuple(book for book in self._books_infos)

    def __eq__(self, other):
        return self._book == other._book


