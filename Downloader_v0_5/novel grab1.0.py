"""使用进程池进行多进程下载，进度条的显示存在一些问题"""
import os
import re
import requests
from multiprocessing import Pool
from bs4 import BeautifulSoup
from multiprocessing import Manager


def main():
    start_url = "https://www.biqooge.com/4_4074/"
    html = get_html(start_url)
    root = './牧神记/'
    set_directory(root)
    if html:
        urls_lis = list()
        get_urls(html, urls_lis, start_url)

        queue = Manager().Queue()
        pool = Pool(5)
        for i in urls_lis:
            pool.apply_async(set_up, args=(root, i, queue,))
        pool.close()

        all_file_num = len(urls_lis)
        count = 0
        while True:
            queue.get()
            count += 1
            print('\r已完成{:.2f}%'.format(count * 100 / all_file_num), end='')
            if count >= all_file_num:
                break
    else:
        print('get html failed')


def get_urls(home_html, urls_lis, start_url):
    soup = BeautifulSoup(home_html, 'html.parser')
    result = soup.find('div', attrs={'id': 'list'})
    urls = re.findall(r'<a href="/4_4074/(.*?)">', str(result))
    for i in range(len(urls)):
        urls_lis.append(start_url + urls[i])


def get_aticle(page_html):
    soup = BeautifulSoup(page_html, 'html.parser')
    article = soup.find("div", attrs={'id': 'content'}).text
    return article


def get_title(html):
    soup = BeautifulSoup(html, 'html.parser')
    result = soup.find('div', attrs={'class': 'bookname'})
    result = result.find('h1').string
    return result


def get_html(url):
    user_info = {'user-agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, timeout=30, headers=user_info)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return False


def set_directory(root):
    try:
        if not os.path.exists(root):
            os.mkdir(root)
    except:
        pass


def set_up(root, url, queue):
    html = get_html(url)
    title = get_title(html)
    content = get_aticle(html)
    path = root + title + '.txt'
    if not os.path.exists(path):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
    queue.put(title)


if __name__ == '__main__':
    main()
