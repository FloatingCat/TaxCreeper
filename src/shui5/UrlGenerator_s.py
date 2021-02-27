import time
import requests
from bs4 import BeautifulSoup
import pandas as pd


class PageReaderForCent(object):

    def __init__(self, url):  # read page from internet
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'Connection': 'keep-alive'
        }
        # self.cookies = 'UM_distinctid=16df733f26b3a8-0c6ae27b1fe39-3d375b01-1fa400-16df733f26c79f; taihe_bi_sdk_uid=cbd969cd52f5f62a6f7fe5069f57cc6c; ngaPassportUid=34337474; ngaPassportUrlencodedUname=%25BD%25D0%25C9%25A7%25B5%25C4%25C3%25A8; ngaPassportCid=Z8eu0qnv7911if6jl6d1alu112qt5v944g00oii6; ngacn0comUserInfo=%25BD%25D0%25C9%25A7%25B5%25C4%25C3%25A8%09%25E5%258F%25AB%25E9%25AA%259A%25E7%259A%2584%25E7%258C%25AB%0942%0942%09%09-10%0922902%094%090%090%0911_-300%2C22_30%2C61_16%2C39_30%2C85_15; CNZZDATA30043604=cnzz_eid%3D1054280295-1571806389-https%253A%252F%252Fwww.google.com%252F%26ntime%3D1574749354; taihe_bi_sdk_session=3f434363b5d97f0bbe5fb22ee06a1e25; ngacn0comUserInfoCheck=6bef3a1628f60ed226b2d9e40cf7b34a; ngacn0comInfoCheckTime=1574750138; lastvisit=1574750762; lastpath=/read.php?tid=19416263&_ff=436; bbsmisccookies=%7B%22uisetting%22%3A%7B0%3A1%2C1%3A1582092365%7D%2C%22pv_count_for_insad%22%3A%7B0%3A-160%2C1%3A1574787652%7D%2C%22insad_views%22%3A%7B0%3A2%2C1%3A1574787652%7D%7D; _cnzz_CV30043604=forum%7Cfid436%7C0'
        # self.cookie = {}
        # for line in self.cookies.split(';'):
        #     name, value = line.strip().split('=', 1)
        #     self.cookie[name] = value
        self.pageurl = url
        res = requests.get(url, headers=self.headers)
        self.soup = BeautifulSoup(res.content, 'html.parser')

    def getTopic(self):
        topics = []
        scored_list = self.soup.find_all('xwt1')
        # topic_list = self.soup.find_all('a', class_='topic')
        for t in scored_list:
            try:
                link_title_span = t.find('div', class_='xwt1_a')  # 标题链接
                link_title=link_title_span.find('a')
                # topic = t.find('a', class_='topic')
                location_span = t.find('xwt1_d', class_='postdate')  # 地址
                location = location_span.find('a').get_text()
                post_date = location_span.find('p',class_='p3').get_text()
                # patternSP = re.compile('.*?相亲.*?')
                # target_str = patternSP.match(topic)
                dict_temp = {
                    'topic': link_title.get_text(),
                    'location': location,
                    'link': 'https://bbs.nga.cn/' + link_title['href'],
                    'postdate': post_date
                }
                topics.append(dict_temp)
            except AttributeError as e:
                print(e)
                continue

        # for t in topic_list:
        #     tempstr=t.get_text()
        #     patternSP = re.compile('.*?相亲.*?')
        #     target_str = patternSP.match(tempstr)
        #     if target_str is not None:
        #         dict_temp={
        #             'topic':tempstr,
        #             'link':'https://bbs.nga.cn/' +t['href']
        #         }
        #         topics.append(dict_temp)#'https://bbs.nga.cn/' + t['href'] + "  " + t.get_text()
        return topics


def GetMultPages(url, number=1):
    DataList = []
    for i in range(1, number + 1):
        print('Processing ' + str(i) + '/' + str(number))
        url_one = url + str(i) + '.html'
        Page_ = PageReaderForCent(url_one)
        DataList.extend(Page_.getTopic())
    DataGenerator(DataList)


def DataGenerator(data):
    dataset = pd.DataFrame(data)
    dataset.to_excel('TestDataShui5.xlsx')


if __name__ == '__main__':
    GetMultPages('https://www.shui5.cn/article/DiFangCaiShuiFaGui/145_', 5)
