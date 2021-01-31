import sqlite3
import pandas


# def ReadCSV():


class DataModel(object):
    def __init__(self):
        self.conn = sqlite3.connect('../data/test.db')
        self.cursor = self.conn.cursor()

    def DoSQL(self, sqlQuery):
        self.cursor.execute(sqlQuery)
        self.conn.commit()

    def CreateDB(self):
        db = sqlite3.connect("../data/test.db")

    def ADD(self):
        preSql = 'InSert '


if __name__ == '__main__':
    db = sqlite3.connect("../data/test.db")
    for c in pandas.read_csv("../dataset.csv", chunksize=3262):
        c.to_sql("dataset", db, if_exists="append")
    db.execute("CREATE INDEX uid ON dataset(C2)")
    db.close()
