class BookStats:
    """
    store the info for one book of downloading
    """
    def __init__(self):
        self.articles_urls = []
        self.sum_tasks = 0
        self.process = 0
        self.completed_articles = []
        self.book = None
        self.book_url = None
        self.books_infos = []

    def __eq__(self, other):
        return self.book == other.book
