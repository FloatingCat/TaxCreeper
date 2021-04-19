import json
import pickle
import sqlite3

import redis
import pandas as pd
from src.config import redis_config

pool = redis.ConnectionPool(host=redis_config['host'], port=redis_config['port'], decode_responses=redis_config['decode_responses'],password=redis_config['password'])
r = redis.Redis(connection_pool=pool)
def picklify(df):
    dt_bytes=pickle.dumps(df)
    return dt_bytes

def res_depicklify_to_list():
    res=[]
    count=r.scard('res_dfs')
    temp_list=[]
    for i in range(count):
        temp=json.loads(r.spop('res_dfs'))
        print(temp)
        temp_list.append(temp)

    # temp_list = r.spop(name='res_dfs',count=r.scard('res_dfs'))
    # print(type(temp_list),temp_list)
    # for temp in temp_list:
    #     print(temp)
    #     res.extend(pickle.load(temp.decode('latin1')))
    data_=pd.DataFrame(temp_list)
    db = sqlite3.connect("t0419.db")
    data_.to_sql("dataset", db, if_exists="append")
    db.close()
    print('Successfully Writen')