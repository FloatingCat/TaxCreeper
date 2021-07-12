import json
from time import sleep

from src.Model.Redis_connecter import RedisConn
from src.controller.config import processing_config
from src.core import Generator_Shui5
import multiprocessing

r = RedisConn().r
core_amount = processing_config['core_amount']*2
max_alloc = processing_config['max_alloc']
min_alloc = processing_config['min_alloc']


def url_put():  # 获得本地队列，根据进程数量*最大本地队列长度申请
    print(r.time())
    temp = r.spop(name='waiting_url', count=core_amount * max_alloc)
    print('temp:', temp)
    return temp


def multi_pages(url_one):
    # print(url_one)
    Page_ = Generator_Shui5.PageReaderForCent(url_one)
    res_page = Page_.getTopic()
    if not res_page:
        return
    res_page_ = json.dumps(res_page)  # 保证原子性和一一对应
    print(type(res_page_), len(res_page_))

    r.hset(name='res_url_set', key=url_one, value=res_page_)
    r.srem('val_url', url_one)  # 删除验证集合


def multi_creeper():  # 根据设定初始化进程池，给进程分配对应任务
    TP = multiprocessing.Pool(int(core_amount))
    url_L = url_put()
    print('urls:', url_L)
    TP.map(multi_pages, url_L)
    TP.close()


def repeater():  # 监听Redis端任务队列，有任务即初始化进程池进行爬取
    while True:
        multi_creeper()
        print('new round')
        sleep(0.5)


if __name__ == '__main__':
    repeater()
