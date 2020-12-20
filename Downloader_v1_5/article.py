import os
import re

from bs4 import BeautifulSoup

from Downloader_v1_5.url_request import UrlRequest


class Article:
    def __init__(self,article_url):
        self.url_request = UrlRequest('gbk')
        self.html = self.url_request.get(article_url)
        self.title = None
        self.content = None

    def get_content(self):
        soup = BeautifulSoup(self.html,'html.parser')
        self.content = soup.find('div',attrs={'id':'content'}).text

    def get_title(self):
        raw_title = re.search(r'<h1>(.*?)</h1>', self.html)[1]
        self.format_title(raw_title)

    def format_title(self,raw_title):
        num_string = '零一二三四五六七八九十百千'
        result = re.search(r"第([%s]*?)章"%num_string, raw_title)
        if result:
            num_list = []
            for i in result.group(1):
                num_list.append(i)
            set_list = ['0', '0', '0', '0']
            if re.search('["十百千"]', result.group(1)):
                dict = {'百': 1, '千': 0, '十': 2}
                for i in range(len(num_list)):
                    if num_list[i] in dict.keys():
                        if i == 0:  # format the num range form ten to twenty
                            set_list[dict[num_list[i]]] = '1'
                        else:
                            set_list[dict[num_list[i]]] = str(num_string.index(num_list[i - 1]))
                if num_list[-1] not in dict.keys():  # format the num like '六百零一'
                    set_list[3] = str(num_string.index(num_list[-1]))
            else:
                # to format the title which doesn't have characters like '十百千'
                num_list.reverse()  # process the situation that the num doesn't have thousand position
                for i in range(len(num_list)):
                    set_list[3 - i] = str(num_string.index(num_list[i]))
            self.title = raw_title.replace(result[1],''.join(set_list))
        else:
            self.title = raw_title

    def write(self,filepath,completed_article,property='.txt'):
        path = os.path.join(filepath,self.title+property)
        with open(path,'w',encoding='utf-8')as f:
            f.write(self.content)
        completed_article.append(f'已下载完....{self.title}')

