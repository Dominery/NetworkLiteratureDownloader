class Settings:
    def __init__(self):
        self.index_url = "https://www.biqooge.com"
        self.search_url = "https://m.biqooge.com/s.php"
        self.select_max = 5
        self.article_urls = []
        self.choose_urls = []
        self.completed_article = []
        self.threads_num = 5
        self.request_head_paras_file = './sources/headers_content'
        self.window_size = (640, 480)
        self.window_title = 'NetworkLiteratureDownloader'
        self.process = 0
        self.sum_tasks = 0

    @property
    def format_process(self):
        return '[{:<20}]已下载:{:.2f}%'.format('#' * (self.process * 20 // self.sum_tasks),
                                            self.process / self.sum_tasks * 100)

    def rest(self):
        self.process = 0
        self.sum_tasks = 0
        self.article_urls = []
        self.choose_urls = []
