import re
import time

import multiprocessing
import requests
from bs4 import BeautifulSoup
import pandas as pd
from src.Model import DataModel
import threading
from greenlet import greenlet


class PageReaderForCent(object):

    def __init__(self, url):  # read page from internet
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'Connection': 'keep-alive'
        }
        self.page_url = url
        res = requests.get(url, headers=self.headers)
        self.soup = BeautifulSoup(res.content, 'html.parser')
        # print('processing:', self.pageurl)

    def getTopic(self):
        print('run in:', multiprocessing.current_process().name)

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
                # print(link_title_span)
                if not link_title_span:
                    link_title_span = t.find('div', class_='xwt2_a')  # 标题链接
                assert link_title_span
                link_title = link_title_span.find('a')
                assert link_title
                # topic = t.find('a', class_='topic')
                location_span = t.find(class_='xwt1_d')  # 地址
                # print(location_span)
                if not location_span:
                    location_span = t.find(class_='xwt2_d')  # 地址
                location = location_span.find('a').get_text()
                post_date = location_span.find('p', class_='p3').get_text()
                link_arc = link_title['href']

                print("link target: ", link_arc)
                res_arc = requests.get(link_arc, headers=self.headers)
                arc_soup = BeautifulSoup(res_arc.content, 'html.parser')
                arc_content = arc_soup.find(class_='arcContent')
                arc_content_str = str(arc_content.get_text()).replace('\r\n', '<br>').replace('\n', '<br>')
                dict_temp = {
                    'topic': link_title.get_text(),
                    'location': location,
                    'link': link_arc,
                    'postdate': post_date,
                    'arc_content': arc_content_str,
                    'Files': GetFile(arc_content)
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
        print('topic_len', len(topics), 'in ', self.page_url)

        return topics


def GetFile(arc_content):
    pdf_links = arc_content.findAll('a', attrs={'href': re.compile('.*?.pdf')})
    doc_links = arc_content.findAll('a', attrs={'href': re.compile('.*?.doc')})
    xls_links = arc_content.findAll('a', attrs={'href': re.compile('.*?.xls')})
    rar_links = arc_content.findAll('a', attrs={'href': re.compile('.*?.rar')})
    pdf_links.extend(doc_links)
    pdf_links.extend(xls_links)  # merge
    pdf_links.extend(rar_links)
    list(pdf_links)
    LinkStr = ''
    if pdf_links is not None:
        for index in range(0, len(pdf_links)):
            linkBuffer = str(pdf_links[index].get('href'))
            linkBuffer_ = 'https://www.shui5.cn' + linkBuffer + '\t<br>'
            LinkStr += linkBuffer_

    return LinkStr


def GetMultiPages(url, number1=1, number2=2):
    def page_run():
        resp = page_instance.getTopic()
        data_list.extend(resp)

    data_list = []
    for i in range(number1, number2 + 1):
        print('Processing ' + str(i) + '/' + str(number2))
        url_one = url + str(i) + '.html'
        print(url_one)
        page_instance = PageReaderForCent(url_one)
        gt = greenlet(page_run())
        gt_res = gt
        # print(gt_res)
        # assert type(gt_res) == list`
        # data_list.extend(gt_res)
    # DataGenerator(data_list)
    print(data_list)
    return data_list


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
    GetMultiPages('https://www.shui5.cn/article/DiFangCaiShuiFaGui/145_', 1, 5)
