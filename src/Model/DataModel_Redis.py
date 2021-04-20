import json
import pickle
import sqlite3
import time
import redis
import pandas as pd

from src.Model.Redis_connecter import RedisConn
from src.controller.config import redis_config


def picklify(df):
    dt_bytes = pickle.dumps(df)
    return dt_bytes


def res_depicklify_to_list():
    r = RedisConn().r
    db = sqlite3.connect("t0419.db")
    res = []
    count = r.scard('res_dfs')
    # temp_list=[]
    temp_list = r.spop('res_dfs', count=count)
    print(temp_list)
    time_start = time.time()
    for item in temp_list:
        temp = json.loads(item)
        print(item)
        res.append(temp)
    time_end = time.time()
    print('de_json used time:', time_end - time_start)
    # pipe=r.pipeline()
    # for i in range(count):
    #     temp=json.loads(r.spop('res_dfs'))
    #     print(temp)
    #     temp_list.append(temp)
    # pipe.execute()
    # temp_list = r.spop(name='res_dfs',count=r.scard('res_dfs'))
    # print(type(temp_list),temp_list)
    # for temp in temp_list:
    #     print(temp)
    #     res.extend(pickle.load(temp.decode('latin1')))
    time_start = time.time()
    data_ = pd.DataFrame(res)
    time_end = time.time()
    print('dataframe used time:', time_end - time_start)
    data_.to_sql("dataset", db, if_exists="append")
    db.close()
    print('Successfully Writen')
