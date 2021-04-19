import pandas as pd
import sqlite3

# TODO:等待重构，将每一页的数据模型优化后的写入该模块（dict很占空间）
def IntoSqlite(data):
    data_=pd.DataFrame(data)
    db = sqlite3.connect("../../testshui5.db")
    data_.to_sql("dataset", db, if_exists="append")
    db.close()
    print('Successfully Writen')