import requests
import json


def turn_headers():
    dict = {}
    with open('headers_content', 'r')as f:
        for line in f:
            line = line.replace('\n', '').replace(' ', '')
            lis = line.split(':')
            if len(lis) == 2:
                dict[lis[0]] = lis[1]
            else:
                content = ''
                for i in range(1, len(lis)):
                    content = content + lis[i]
                dict[lis[0]] = content
    return dict


url = 'https://m.biqooge.com/s.php'
session = requests.Session()
code_json = session.post(url, headers=turn_headers(), data={'keyword': '牧神记', 't': '1'})

print(code_json.text)
