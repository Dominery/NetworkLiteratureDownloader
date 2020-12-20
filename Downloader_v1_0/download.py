import os

from Downloader_v1_0.article import Article
from Downloader_v1_0.book import Book


class Download:
    def __init__(self, book_name):
        self.book = Book(book_name)
        self.article = Article

    def get_article_urls(self):
        self.book.get_book_info()
        self.book.make_choice()
        self.book.get_urls_article()

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

    def download(self, directory_path):
        self.get_article_urls()
        self.mkdir(directory_path)
        sum_articles = len(self.book.article_urls)
        for i in range(sum_articles):
            self.make_article(self.book.article_urls[i])
            format_process = '\r[{:<20}]已下载:{:.2f}%'.format('#' * (i * 20 // sum_articles), i / sum_articles)
            print(format_process, end='')


def main():
    down = Download('牧神记')
    down.download('./')


if __name__ == '__main__':
    main()
