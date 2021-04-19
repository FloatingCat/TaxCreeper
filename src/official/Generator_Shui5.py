import os
import re
import time

import multiprocessing
import requests
from bs4 import BeautifulSoup
import pandas as pd
from src.utils import DataModel


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
        # print('processing:', self.pageurl)

    def getTopic(self):
        print('run in:',multiprocessing.current_process().name)

        topics = []
        scored_list = self.soup.find_all(class_='xwt1')
        if not scored_list:
            scored_list = self.soup.find_all(class_='xwt2')
        # print('list:',scored_list)
        # topic_list = self.soup.find_all('a', class_='topic')
        for t in scored_list:
            time_start = time.time()
            try:
                link_title_span = t.find('div', class_='xwt1_a')  # 标题链接
                #print(link_title_span)
                if not link_title_span:
                    link_title_span = t.find('div', class_='xwt2_a')  # 标题链接
                link_title = link_title_span.find('a')
                # topic = t.find('a', class_='topic')
                location_span = t.find(class_='xwt1_d')  # 地址
                #print(location_span)
                if not location_span:
                    location_span = t.find(class_='xwt2_d')  # 地址
                location = location_span.find('a').get_text()
                post_date = location_span.find('p', class_='p3').get_text()
                # patternSP = re.compile('.*?相亲.*?')
                # target_str = patternSP.match(topic)

                link_arc = link_title['href']
                res_arc = requests.get(link_arc, headers=self.headers)
                arc_soup = BeautifulSoup(res_arc.content, 'html.parser')
                arcContent = arc_soup.find(class_='arcContent')
                arcContent_str = str(arcContent.get_text()).replace('\r\n', '<br>').replace('\n', '<br>')
                dict_temp = {
                    'topic': link_title.get_text(),
                    'location': location,
                    'link': link_arc,
                    'postdate': post_date,
                    'arcContent': arcContent_str,
                    'Files': GetFile(arcContent)
                }
                # print(dict_temp['topic'])
                # print(topics)
                topics.append(dict_temp)
                # print(dict_temp)
                time_end = time.time()
                # print('totally cost', time_end - time_start)
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
        print('topic_len',len(topics),'in ',self.pageurl)


        return topics


def GetFile(arcContent):
    PDFlinks = arcContent.findAll('a', attrs={'href': re.compile('.*?.pdf')})
    DOClinks = arcContent.findAll('a', attrs={'href': re.compile('.*?.doc')})
    XLSlinks = arcContent.findAll('a', attrs={'href': re.compile('.*?.xls')})
    RARlinks = arcContent.findAll('a', attrs={'href': re.compile('.*?.rar')})
    PDFlinks.extend(DOClinks)
    PDFlinks.extend(XLSlinks)  # merge
    PDFlinks.extend(RARlinks)
    list(PDFlinks)
    LinkStr = ''
    if PDFlinks is not None:
        for index in range(0, len(PDFlinks)):
            linkBuffer = str(PDFlinks[index].get('href'))
            linkBuffer_ = 'https://www.shui5.cn' + linkBuffer + '\t<br>'
            LinkStr += linkBuffer_

    return LinkStr


def GetMultPages(url, number1=1, number2=2):
    DataList = []
    for i in range(number1, number2 + 1):
        print('Processing ' + str(i) + '/' + str(number2))
        url_one = url + str(i) + '.html'
        print(url_one)
        Page_ = PageReaderForCent(url_one)
        DataList.extend(Page_.getTopic())
    # DataGenerator(DataList)
    return DataList


# def GetOnePage(url):
#     print('processing '+url)
#     print(url_one)
#     Page_ = PageReaderForCent(url_one)
#     return DataList

def DataGenerator(data):
    dataset = pd.DataFrame(data)
    # dataset.to_excel('TestDataShui5.xlsx')
    DataModel.IntoSqlite(dataset)


if __name__ == '__main__':
    GetMultPages('https://www.shui5.cn/article/DiFangCaiShuiFaGui/145_', 5)
