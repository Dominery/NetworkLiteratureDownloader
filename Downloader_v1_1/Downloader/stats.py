class Stats:
    """
    store the info for one book of downloading
    """
    def __init__(self,book):
        self.articles_urls = []
        self.sum_tasks = 0
        self.process = 0
        self.completed_articles = []
        self.book = book
        self.books_urls = []
