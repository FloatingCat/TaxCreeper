import json

from time import sleep

import redis
import pickle

from src.config import redis_config
from src.core import Generator_Shui5
import multiprocessing

res_list = []
pool = redis.ConnectionPool(host=redis_config['host'], port=redis_config['port'],
                            decode_responses=redis_config['decode_responses'], password=redis_config['password'])
r = redis.Redis(connection_pool=pool)
core_amount = multiprocessing.cpu_count()
max_alloc = 4
min_alloc = 2


def url_put():
    print(r.time())
    # for i in range(core_amount * max_alloc):
    #     temp = r.spop('waiting_url')
    #     if not temp:
    #         print('stop at_:', r.time())
    #         return 'stop'
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


def multi_creeper():
    TP = multiprocessing.Pool(core_amount)
    url_L = url_put()
    print('urls:', url_L)
    TP.map(multi_pages, url_L)
    TP.close()


if __name__ == '__main__':
    while True:
        # url_put()
        multi_creeper()
        print('new round')
        sleep(0.5)
    # url_put()
    # multi_creeper()
    # sleep(0.5)
