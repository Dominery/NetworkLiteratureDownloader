import os
import re


from Downloader_v1_0.url_request import UrlRequest


class Article:
    def __init__(self,article_url):
        self.url_request = UrlRequest('utf-8')
        self.html = self.url_request.get(article_url)
        self.title = None
        self.content = None

    def get_content(self):
        self.content = re.search(r'<div id="content">(.*?)</div>',self.html)[1]

    def get_title(self):
        raw_title = re.search(r'<h1>(.*?)</h1>', self.html)[1]
        self.format_title(raw_title)

    def format_title(self,raw_title):
        num_string = '零一二三四五六七八九十百千'
        result = re.search(f"第([{num_string}]*?)章(.*?).txt", raw_title)
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
            self.title = '第' + ''.join(set_list) + '章' + result.group(2)
        else:
            self.title = raw_title

    def write(self,filepath):
        path = os.path.join(filepath,self.title)
        with open(path,'w',encoding='utf-8')as f:
            f.write(self.content)

