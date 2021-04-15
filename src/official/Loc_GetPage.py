# -*- coding : utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup
from src.utils import UrlReader


class PageReaderForLoc(object):
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
            valid = self.PageContent.find(attrs={'style': 'color: #df0000;margin-right: 15px;'}).getText()
        except AttributeError as redirectErr:
            # print(str(self.pageurl) + " occurs error")
            # print(redirectErr)
            return '全文有效' #yunnan
        else:
            # print(valid)
            if str(valid) == '全文有效':
                # print('Yes')
                return '全文有效'
            else:
                # print('No')
                return valid

    def GetTitle(self):
        pagetitle = self.PageContent.find(class_='title').getText()
        return str(pagetitle)

    def GetSerialNum(self):
        serialnum = self.PageContent.find(text=re.compile('.*?年.*?第.*?号.*?'))
        return str(serialnum)

    def GetPublishDate(self):
        temp = self.PageContent.find(text=re.compile('.*?\\d\\d\\d\\d-\\d\\d-\\d\\d.*?'))
        timestamp = str(temp)
        if timestamp == '': return False
        return timestamp

    def WriteData(self, Filter):  # format content string
        tempstr = ''
        for index in Filter:
            tempstr += str(index.get_text()).replace('\r\n',
                                                     '<br>')  # .replace('<strong>', '').replace('</strong>', '')
            tempstr.replace('\n', '<br>').replace('\n注释：\n\n', '').replace('网站纠错', '')
        return tempstr

    def pattern_first(self):  # fontzoom -> p
        tempstr = ''
        divFilter = self.PageContent.find(id='zoom')
        pFilter = divFilter.findAll('p')
        return self.WriteData(pFilter)

    # TODO:class="TextContentDuanLuo"
    # TODO:重构
    def GetDivContent(self):
        ContentStr = self.pattern_first()
        # print(ContentStr)
        return ContentStr

    # Get links of pdf,doc/docx,xls/xlsx
    def GetFile(self):
        PDFlinks = self.PageContent.findAll('a', attrs={'href': re.compile('.*?.pdf')})
        DOClinks = self.PageContent.findAll('a', attrs={'href': re.compile('.*?.doc')})
        XLSlinks = self.PageContent.findAll('a', attrs={'href': re.compile('.*?.xls')})
        RARlinks = self.PageContent.findAll('a', attrs={'href': re.compile('.*?.rar')})
        PDFlinks.extend(DOClinks)
        PDFlinks.extend(XLSlinks)  # merge
        PDFlinks.extend(RARlinks)
        list(PDFlinks)
        LinkStr = ''
        if PDFlinks is not None:
            for index in range(0, len(PDFlinks)):
                linkBuffer = str(PDFlinks[index].get('href'))
                linkBuffer_ = str(self.pageurl).rsplit('content.html')[0] + linkBuffer + '\t<br>'
                # PDFlinks[index] = linkBuffer_
                LinkStr += linkBuffer_

        return LinkStr

    # TODO:id,inset time,serial number,file name,file content,publish time,validity,attachment
    # Model
    def GetSingePage(self, loc='undefined'):
        vali = self.Validity()
        if vali != '无效网址':

            ResSet = {
                'SerialNum': self.GetSerialNum(),
                'PageTitle': self.GetTitle(),
                'PublishDate': self.GetPublishDate(),
                'Content': self.GetDivContent(),
                'FileUrlSet': self.GetFile(),
                'OriginalURL': self.pageurl,
                'Location': loc,
                'Valid': vali
            }
            return ResSet
        else:
            return None


# TODO:多地区
def GetAllinArea(filename='../data/sichuan.txt'):
    UrlLists = UrlReader.UrlReader(filename)
    length = len(UrlLists)
    ALLDATA = []
    filename=filename.replace('../data/','').replace('.txt','')
    print(filename)
    for index in range(0, len(UrlLists)):
        print("process: " + str(index + 1) + "/" + str(length))
        PR = PageReaderForLoc(UrlLists[index])
        res = PR.GetSingePage(filename)
        if res is not None and PR.Validity() != '无效网址':
            ALLDATA.append(res)
        else:
            print('Invalid page in ' + str(UrlLists[index]))

    return ALLDATA


def GetAllinLoc():
    ALLDATA = []
    LocList=['../data/sichuan.txt','../data/yunnan.txt']
    for i in LocList:
        ALLDATA.extend(GetAllinArea(i))
    return ALLDATA


if __name__ == '__main__':
    print(GetAllinLoc())
    print("Finished!")
