# -*- coding : utf-8 -*-
import re
import time
import requests
from bs4 import BeautifulSoup
from src import UrlReader

class PageReaderForCent(object):
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
            return '无效网址'
        else:
            # print(valid)
            if str(valid) == '全文有效':
                # print('Yes')
                return '全文有效'
            else:
                # print('No')
                return valid

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
            tempstr.replace('\n', '<br>').replace('\n注释：\n\n', '').replace('网站纠错','')
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
        # ContentStr = self.pattern_first()
        # if len(ContentStr) == 0:
        #     ContentStr = self.pattern_third()
        #     if len(ContentStr) == 0:
        #         ContentStr = self.pattern_forth()
        # if len(ContentStr) == 0:
        #     print(self.pageurl + " Empty Content?")
        #     ContentStr = 'Empty!!!'
        ContentStr = self.pattern_first()+self.pattern_third()+self.pattern_forth()

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
                LinkStr +=linkBuffer_

        return LinkStr

    # TODO:id,inset time,serial number,file name,file content,publish time,validity,attachment
    # Model
    def GetSingePage(self):
        vali=self.Validity()
        if vali != '无效网址':

            ResSet = {
                'SerialNum': self.GetSerialNum(),
                'PageTitle': self.GetTitle(),
                'PublishDate': self.GetPublishDate(),
                'Content': self.GetDivContent(),
                'FileUrlSet': self.GetFile(),
                'OriginalURL': self.pageurl,
                'Location': 'Center',
                'Valid':vali
            }
            # ResSet = [
            #     self.GetSerialNum(),
            #     self.GetTitle(),
            #     self.GetPublishDate(),
            #     self.GetDivContent(),
            #     self.GetFile(),
            #     self.pageurl]
            return ResSet
        else:
            return None


def GetAllinCent(filename='../data/textone.txt'):
    # UrlLists = UrlReader('data_url.txt')
    # UrlLists = UrlReader.UrlReader('textone.txt')
    UrlLists = UrlReader.UrlReader(filename)
    length = len(UrlLists)
    PR = PageReaderForCent(UrlLists[0])
    res = PR.GetSingePage()
    # ALLDATA_ = pd.DataFrame(columns=("SerialNum", "PageTitle", "PublishDate", "Content", "FileUrlSet", "OriginalURL"))
    ALLDATA=[]

    for index in range(0,len(UrlLists)):
        print("process: " + str(index+1) + "/" + str(length))
        PR = PageReaderForCent(UrlLists[index])
        res = PR.GetSingePage()
        # print(res)
        if res is not None and PR.Validity() != '无效网址':
            ALLDATA.append(res)
            # ALLDATA_.append(pd.Series(res),ignore_index=True)
            # DataDict.update(res)
            # print(oneurl + ' Finished!')
        else:
            print('Invalid page in ' + str(UrlLists[index]))
            # print(res)
    # ALLDATA_=pd.DataFrame(ALLDATA)
    # db = sqlite3.connect("test.db")
    # ALLDATA_.to_sql("dataset", db, if_exists="append")
    # db.close()
    return ALLDATA


if __name__ == '__main__':
    print(GetAllinCent())
    print("Finished!")

