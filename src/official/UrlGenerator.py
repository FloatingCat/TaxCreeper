import re

import requests
from bs4 import BeautifulSoup


def UGenerator(data=None, location='unname'):
    if data is None:
        print('No data!')
        return False
    print('Generating')
    with open('../../data/' + location + '.txt', 'w') as DataFile:
        for item in data:
            DataFile.write(item)
            DataFile.write('\n')


def ProcessCN():  # 总局
    url = 'http://www.chinatax.gov.cn/api/query?siteCode=bm29000fgk&tab=all&key=9A9C42392D397C5CA6C1BF07E2E0AA6F'
    UList = []
    with open('../../data_url.txt', 'w') as DataFile:
        for i in range(1, 406):
            data = requests.get(url,
                                params={"timeOption": "2",
                                        "page": str(i),
                                        "pageSize": "10",
                                        "keyPlace": "1",
                                        "qt": "*",
                                        "startDateStr": "1978-01-01",
                                        "endDateStr": "2021-01-30",
                                        "sort": 'dateDesc'}).json()
            mylist = data['resultList']
            for item in mylist:
                UList.append(item['url'])
                DataFile.write(item['url'])
                DataFile.write('\n')



def ProcessLoc(loc,url,total):
    templist = []

    for index in range(1, total + 1):
        tempurl = url + str(index)
        # print(tempurl)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 '
                          'Safari/537.36 '
        }
        page = requests.get(tempurl, headers)
        PageContent = BeautifulSoup(page.content, 'html.parser')
        aContent = PageContent.find_all('a', target="_blank")
        for a in aContent:
            linkbuffer = str(a.get('href'))
            patternGOV=re.compile('.*?www\.yn\.gov\.cn.*?')
            linkGov = patternGOV.match(linkbuffer)
            if linkGov == None:
                linkbuffer='https://'+loc+'.chinatax.gov.cn'+linkbuffer.replace('../..','')
            else :
                linkbuffer=linkbuffer.replace('../../','')
                break
            # print(linkGov)
            templist.append(linkbuffer)
    print(len(templist))
    return templist



def ProcessLocal():
    locationDict={
        'sichuan':'https://sichuan.chinatax.gov.cn/module/search/index.jsp?field=vc_name:1:0,field_302:1:0,field_309:7:0,field_314:1:0,field_315:1:0,field_316:1:0,field_384:10:0&i_columnid=8803&field_384,0_start=&field_384,0_end=&vc_name=&field_302=&field_314=&field_315=&field_316=&field_309,0=&currpage=',
        'yunnan':'https://yunnan.chinatax.gov.cn/module/search/index.jsp?field=vc_name:1:0,vc_keyword:1:0,c_deploytime:3:0,field_451:1:0,field_530:7:0,field_523:12:0,field_681:12:0,field_682:12:0&i_columnid=3908&c_deploytime_start=&c_deploytime_end=&vc_name=&vc_keyword=&field_451=&field_530,0=&field_523=%E8%AF%B7%E9%80%89%E6%8B%A9&field_681=%E8%AF%B7%E9%80%89%E6%8B%A9&field_682=1&currpage=',
        'liaoning':'http://liaoning.chinatax.gov.cn/module/search/index.jsp?field=vc_name:1:0,field_1252:1:0,field_1265:1:1,field_1266:1:0,field_1267:1:0,field_1273:7:0,field_1274:1:1,field_1476:3:1&i_columnid=style_16&field_1476_start=&field_1476_end=&vc_name=&field_1252=&field_1265=&field_1266=%E8%BE%BD%E5%AE%81%E7%9C%81%E7%A8%8E%E5%8A%A1%E5%B1%80&field_1267=&field_1274=&field_1273=&currpage='
    }
    keys = locationDict.keys()
    for item in locationDict:
        # print(item)
        # print(locationDict[item])
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 '
                          'Safari/537.36 '
        }
        page = requests.get(locationDict[item]+'1', headers)
        PageContent = BeautifulSoup(page.content, 'html.parser')
        pageAmount=str(PageContent.find('span',attrs={'style': 'padding-left:8px;'}).getText())
        amount=int(re.findall(r'\d+',pageAmount)[0]) # 仅需要数字
        print(amount)
        # Amount=pageAmount.split('\r')[1]
        UGenerator(ProcessLoc(item,locationDict[item],amount),item)
        print(item)



if __name__ == '__main__':

    ProcessLocal()
