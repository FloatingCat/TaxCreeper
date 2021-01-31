import pandas as pd
import sqlite3

def IntoSqlite(data):
    data_=pd.DataFrame(data)
    db = sqlite3.connect("../data/test.db")
    data_.to_sql("dataset", db, if_exists="append")
    db.close()
    print('Successfully Writen')