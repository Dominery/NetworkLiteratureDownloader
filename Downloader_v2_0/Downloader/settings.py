class Settings:
    def __init__(self):
        self.index_url = "https://www.biqooge.com"
        self.search_url = "https://m.biqooge.com/s.php"
        self.select_max = 5
        self.threads_num = 5
        self.gevent_pool_num = 10
        self.request_head_paras_file = './sources/headers_content'
        self.window_title = 'NetworkLiteratureDownloader'
        self.store_directory_path = None
