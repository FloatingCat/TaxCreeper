import requests
from bs4 import BeautifulSoup
import re


def pagetest(url):
    pageurl = url
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 '
                      'Safari/537.36 '
    }
    page = requests.get(url, headers)
    PageContent = BeautifulSoup(page.content, 'html.parser')
    print(PageContent)
    temp = PageContent.find(text=re.compile('.*?\\d\\d\\d\\d-\\d\\d-\\d\\d.*?'))

    print(temp)
    # timestamp = temp.find()


if __name__ == '__main__':
    pagetest('https://sichuan.chinatax.gov.cn/art/2020/3/16/art_8803_8486.html')
