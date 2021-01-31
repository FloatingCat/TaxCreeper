# -*- coding : utf-8 -*-
import csv
import json
import re
import time

import requests
from bs4 import BeautifulSoup


# Read Url
def UrlReader(FileName):
    with open(FileName) as f:
        UrlLists = f.read().splitlines()
        return UrlLists


class PageReader(object):
    def __init__(self, url):  # read page from internet
        self.pattern = 0
        self.pageurl = url
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 '
                          'Safari/537.36 '
        }
        page = requests.get(url, headers)
        self.PageContent = BeautifulSoup(page.content, 'html.parser')
        delC = self.PageContent.find(id="tk-container-2020")  # a bunch of ****
        if delC:
            delC.decompose()

    def Validity(self):  # if it is out of date
        try:
            valid = self.PageContent.find(id='yxq-tip').getText()
        except AttributeError as redirectErr:
            print(str(self.pageurl) + " occurs error")
            print(redirectErr)
            return False
        else:
            # print(valid)
            if str(valid) == '全文有效':
                # print('Yes')
                return True
            else:
                # print('No')
                return False

    def GetTitle(self):
        pagetitle = self.PageContent.find(class_='dhgao title1').getText()
        return str(pagetitle)

    def GetSerialNum(self):
        serialnum = self.PageContent.find(class_='hao1').getText()
        return str(serialnum)

    def GetPublishDate(self):
        timestamp = self.PageContent.find(id='data').getText()  # 1381419600
        if timestamp == '': return False
        timeStamp = int(timestamp) / 1000
        if timeStamp == '':
            return timestamp
        timeArray = time.localtime(timeStamp)
        otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
        #  print(otherStyleTime)  # 2013--10--10 23:40:00
        return otherStyleTime

    def WriteData(self, Filter):
        tempstr = ''
        for index in Filter:
            tempstr += str(index.get_text()).replace('\r\n',
                                                     '<br>')  # .replace('<strong>', '').replace('</strong>', '')
            tempstr.replace('\n', '<br>').replace('\n注释：\n\n', '')
        return tempstr

    def pattern_first(self):  # fontzoom -> p
        tempstr = ''
        divFilter = self.PageContent.find(id='fontzoom')
        pFilter = divFilter.findAll('p')
        return self.WriteData(pFilter)

    def pattern_second(self):  # p-style
        pInStyleFilter = self.PageContent.findAll('p', attrs={
            'style': 'text-indent: 2em; text-align: justify;'})  # style Filter for normal situation
        return self.WriteData(pInStyleFilter)

    def pattern_third(self):  # div-class
        divFilter = self.PageContent.find(id='fontzoom')
        divFilter2 = divFilter.findAll(class_='TextContentDuanLuo')
        return self.WriteData(divFilter2)

    def pattern_forth(self):  # div-class
        divFilter = self.PageContent.find(id='fontzoom')
        divFilter2 = divFilter.findAll('div')
        return self.WriteData(divFilter2)

    # TODO:class="TextContentDuanLuo"
    # TODO:重构
    def GetDivContent(self):
        # self.PageContent.findAll('h3').clear()
        ContentStr = self.pattern_first()
        if len(ContentStr) == 0:
            ContentStr = self.pattern_third()
            if len(ContentStr) == 0:
                ContentStr = self.pattern_forth()
        # print(ContentStr)
        if len(ContentStr) == 0:
            print(self.pageurl + " Empty Content?")
            ContentStr = 'Empty!!!'
        # print(ContentStr)
        return ContentStr

    # Get links of pdf,doc/docx,xls/xlsx
    def GetFile(self):
        PDFlinks = self.PageContent.findAll('a', attrs={'href': re.compile('.*?.pdf')})
        DOClinks = self.PageContent.findAll('a', attrs={'href': re.compile('.*?.doc')})
        XLSlinks = self.PageContent.findAll('a', attrs={'href': re.compile('.*?.xls')})
        PDFlinks.extend(DOClinks)
        PDFlinks.extend(XLSlinks)  # merge
        list(PDFlinks)
        if PDFlinks is not None:
            for index in range(0, len(PDFlinks)):
                linkBuffer = str(PDFlinks[index].get('href'))
                # print(linkBuffer)
                linkBuffer_ = str(self.pageurl).rsplit('content.html')[0] + linkBuffer
                # print("link:" + linkBuffer_)
                PDFlinks[index] = linkBuffer_
        # if not PDFlinks: print('No File in ' + self.pageurl)
        return PDFlinks

    # TODO:id,inset time,serial number,file name,file content,publish time,validity,attachment
    # Model
    def GetSingePage(self):
        if self.Validity() == True:
            ResSet = {
                'SerialNum': self.GetSerialNum(),
                'PageTitle': self.GetTitle(),
                'PublishDate': self.GetPublishDate(),
                'Content': self.GetDivContent(),
                'FileUrlSet': self.GetFile(),
                'OriginalURL': self.pageurl
            }
            return ResSet
        else:
            return None


def GetOne(Url):
    # UrlLists = UrlReader('data_url.txt')
    # Url = UrlLists[0]
    dict = {}
    PR = PageReader(Url)
    res = PR.GetSingePage()
    with open('../singleTest.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["SerialNum", "PageTitle", "PublishDate", "Content", "FileUrlSet",
                                                  "OriginalURL"])
        writer.writeheader()
        if res is not None:
            writer.writerow(res)
            print(Url + ' Finished!')
        else:
            print('Invalid page in ' + str(Url))
        print(res)
        file.close()


def GetAllToCSV():
    UrlLists = UrlReader('../data_url.txt')
    length = len(UrlLists)
    with open('../dataset.csv', 'w', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["SerialNum", "PageTitle", "PublishDate", "Content", "FileUrlSet",
                                                  "OriginalURL"])
        writer.writeheader()
        for index, oneurl in enumerate(UrlLists):
            print("process: " + str(index) + "/" + str(length))
            PR = PageReader(oneurl)
            res = PR.GetSingePage()
            if res is not None and PR.Validity() == True:
                writer.writerow(res)
                # DataDict.update(res)
                # print(oneurl + ' Finished!')
            else:
                print('Invalid page in ' + str(oneurl))
            # print(res)
        file.close()


def GetOnetoJSON(Url):
    dict_list = []
    PR = PageReader(Url)
    res = PR.GetSingePage()
    if res is not None and PR.Validity() == True:
        dict_list.append(res)
    else:
        print('Invalid page in ' + str(Url))
    with open('../JsonDataSet.json', mode='w') as f:
        json.dump(dict_list, f)
        f.close()


def GetAlltoJSON():
    UrlLists = UrlReader('../data_url.txt')
    length = len(UrlLists)
    dict_list = []
    for index, oneurl in enumerate(UrlLists):
        print("process: " + str(index) + "/" + str(length))
        PR = PageReader(oneurl)
        res = PR.GetSingePage()
        if res is not None and PR.Validity() == True:
            dict_list.append(res)
        else:
            print('Invalid page in ' + str(oneurl))
    with open('../JsonDataSet.json', mode='w') as f:
        json.dump(dict_list, f)
        f.close()
        # print(res)


def JsonReader(filename):
    with open(filename, mode='r') as f:
        dict = json.load(f)
        for item in dict:
            print(item)


if __name__ == '__main__':
    # UrlLists = UrlReader('data_url.txt')
    # print('Start page testing!')
    # GetOne('http://www.chinatax.gov.cn/chinatax/n370/c5135352/content.html')
    GetAllToCSV()
    # GetAlltoJSON()
    # GetOnetoJSON('http://www.chinatax.gov.cn/chinatax/n360/c157668/content.html')
    # JsonReader('JsonDataSet.json')
    print("Finished!")
    # PR = PageReader(UrlLists[0])
    # PR.GetSingePage()
    # print(UrlLists[0])
