import os
import re
import requests
from multiprocessing.dummy import Pool
from bs4 import BeautifulSoup

count = 0


def main():
    start_url = "https://www.biqooge.com/4_4074/"
    html = get_html(start_url)
    if html:
        urls_lis = []
        get_urls(html, urls_lis, start_url)
        pool = Pool(15)
        pool.map(set_up, urls_lis)
    else:
        print('get html failed')


def get_urls(home_html, urls_lis, start_url):
    global num
    soup = BeautifulSoup(home_html, 'html.parser')
    result = soup.find('div', attrs={'id': 'list'})
    urls = re.findall(r'<a href="/4_4074/(.*?)">', str(result))
    for i in range(len(urls)):
        urls_lis.append(start_url + urls[i])
    num = len(urls_lis)


def get_aticle(url):
    page_html = get_html(url)
    soup = BeautifulSoup(page_html, 'html.parser')
    article = soup.find("div", attrs={'id': 'content'}).text
    return article


def get_title(url):
    html = get_html(url)
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


def set_up(url):
    root = './牧神记/'
    global count
    count += 1
    try:
        if not os.path.exists(root):
            os.mkdir(root)
        else:
            title = get_title(url)
            content = get_aticle(url)
            path = root + title + '.txt'
            if not os.path.exists(path):
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
            print('\r已完成{:.2f}%'.format(count * 100 / num), end='')
    except:
        pass


if __name__ == '__main__':
    main()
