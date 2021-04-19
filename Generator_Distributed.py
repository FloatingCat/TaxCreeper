import json
from time import sleep

import redis
import pickle

from src.config import redis_config
from src.core import Generator_Shui5
import multiprocessing

# url_que = multiprocessing.Queue()

res_list = []
# pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
# pool = redis.ConnectionPool(host='39.97.175.209', port=6379, decode_responses=True,password='x74rtw05')
pool = redis.ConnectionPool(host=redis_config['host'], port=redis_config['port'],
                            decode_responses=redis_config['decode_responses'], password=redis_config['password'])
r = redis.Redis(connection_pool=pool)
core_amount = 32
max_alloc = 4
min_alloc = 2
# manager = multiprocessing.Manager()
# url_que = multiprocessing.Queue()
url_L = []


def url_put():
    print(r.time())
    # for i in range(core_amount * max_alloc):
    #     temp = r.spop('waiting_url')
    #     if not temp:
    #         print('stop at_:', r.time())
    #         return 'stop'
    temp = r.spop(name='waiting_url', count=core_amount * max_alloc)
    print('temp:', temp)
    url_L.extend(temp)


def multi_pages(url_one):
    # print(url_one)
    Page_ = Generator_Shui5.PageReaderForCent(url_one)
    res_page = Page_.getTopic()
    if not res_page:
        return
    for item in res_page:
        temp = json.dumps(item)
        r.sadd('res_dfs',temp)
    # print(len(res_page), res_page)
    # res_bytes = pickle.dumps(res_page) # List 压成 pickle
    # print(res_bytes)
    # r.sadd('res_dfs', res_bytes)
    # res_list.extend(Page_.getTopic())


def multi_creeper():
    res_stat = None
    # url_waiting=[]
    TP = multiprocessing.Pool(core_amount)
    # while url_que.qsize()!=0:
    #     url_waiting.append(url_que.get())
    print(url_L)
    TP.map(multi_pages, url_L)
    # while not url_que.empty():
    #     if url_que.qsize() <= core_amount * min_alloc and res_stat != 'stop':
    #         print('que_size:', url_que.qsize())
    #         res_stat = url_put(url_que)
    #
    #     now_url = url_que.get()
    #     print('now:', now_url)
    #     TP.apply_async(func=multi_pages(now_url))
    #     # if res_stat == 'stop':
    #     #     print('stop at',url_que.qsize())
    #     #     break
    # TP.close()
    # TP.join()
    # # DataModel.IntoSqlite(pd.DataFrame(res_list))
    # df_bytes=pickle.dumps(pd.DataFrame(res_list))
    # r.sadd('res_dfs',df_bytes)
    TP.close()


if __name__ == '__main__':
    while True:
        url_put()
        multi_creeper()
        print('new round')
        sleep(0.5)
    # url_put()
    # multi_creeper()
    # sleep(0.5)
