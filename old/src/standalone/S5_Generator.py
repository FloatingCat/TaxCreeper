from time import sleep

from old.src.core import Generator_Shui5
from old.src.Model import DataModel
import multiprocessing
import pandas as pd

url_que = multiprocessing.Queue()
res_list = []


def url_put():
    for i in range(1, 602):
        url_que.put('https://www.shui5.cn/article/NianDuCaiShuiFaGui/108_' + str(i))
    for i in range(1, 962):
        url_que.put('https://www.shui5.cn/article/DiFangCaiShuiFaGui/145_' + str(i))


def multi_pages(url_one):
    Page_ = Generator_Shui5.PageReaderForCent(url_one)
    res_list.extend(Page_.getTopic())


def multi_creeper():
    TP = multiprocessing.Pool(8)
    while not url_que.empty():
        TP.apply_async(multi_pages(url_que.get()))
    TP.close()
    TP.join()
    DataModel.IntoSqlite(pd.DataFrame(res_list))


if __name__ == '__main__':
    while True:
        url_put()
        multi_creeper()
        sleep(2)
