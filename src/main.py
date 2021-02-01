import time

from src import DataModel, CN_GetPage, Loc_GetPage,UrlGenerator
import threading

# TODO:多线程优化
threadLock = threading.Lock()
threads = []
exitFlag = 0
datalist = []


class Thread_Center(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("开始线程：" + self.name)
        # print_time(self.name, self.counter, 5)
        data = (CN_GetPage.GetAllinCent('../data/textone.txt'))
        # small test
        # data.extend(data)
        threadLock.acquire()
        datalist.extend(data)

        threadLock.release()
        print(data)
        print("退出线程：" + self.name)


class Thread_Loc1(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("开始线程：" + self.name)
        # print_time(self.name, self.counter, 5)
        data = (Loc_GetPage.GetAllinLoc())
        # small test
        # data.extend(data)
        threadLock.acquire()  # lock

        datalist.extend(data)

        threadLock.release()
        print(data)
        print("退出线程：" + self.name)


if __name__ == '__main__':
    # data=(CN_GetPage.GetAllinCent('../data/data_url.txt'))
    # # small test
    # # data.extend(data)
    #
    # DataModel.IntoSqlite(data)
    # print(data)
    thread2 = Thread_Loc1(2, 'Loc1', 2)
    thread1 = Thread_Center(1, 'Center', 1)
    thread2.start()
    thread1.start()
    # threads.append(thread1)
    thread2.join()
    thread1.join()
    print('All thread off')
    print(datalist)
    DataModel.IntoSqlite(datalist)
