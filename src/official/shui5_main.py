from src.official import Generator_Shui5
from src.utils import DataModel
import threading

# TODO:多线程优化
threadLock = threading.Lock()
threads = []
exitFlag = 0
datalist = []


class Thread_Center1(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("开始线程：" + self.name)
        # print_time(self.name, self.counter, 5)
        data = (Generator_Shui5.GetMultPages('https://www.shui5.cn/article/NianDuCaiShuiFaGui/108_',500,604))
        # small test
        # data.extend(data)
        threadLock.acquire()
        datalist.extend(data)

        threadLock.release()
        print(data)
        print("退出线程：" + self.name)

class Thread_Center2(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("开始线程：" + self.name)
        # print_time(self.name, self.counter, 5)
        data = (Generator_Shui5.GetMultPages('https://www.shui5.cn/article/NianDuCaiShuiFaGui/108_',400,499))
        # small test
        # data.extend(data)
        threadLock.acquire()
        datalist.extend(data)

        threadLock.release()
        print(data)
        print("退出线程：" + self.name)

class Thread_Center3(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("开始线程：" + self.name)
        # print_time(self.name, self.counter, 5)
        data = (Generator_Shui5.GetMultPages('https://www.shui5.cn/article/NianDuCaiShuiFaGui/108_',300,399))
        # small test
        # data.extend(data)
        threadLock.acquire()
        datalist.extend(data)

        threadLock.release()
        print(data)
        print("退出线程：" + self.name)

class Thread_Center4(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("开始线程：" + self.name)
        # print_time(self.name, self.counter, 5)
        data = (Generator_Shui5.GetMultPages('https://www.shui5.cn/article/NianDuCaiShuiFaGui/108_',200,299))
        # small test
        # data.extend(data)
        threadLock.acquire()
        datalist.extend(data)

        threadLock.release()
        print(data)
        print("退出线程：" + self.name)

class Thread_Center5(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("开始线程：" + self.name)
        # print_time(self.name, self.counter, 5)
        data = (Generator_Shui5.GetMultPages('https://www.shui5.cn/article/NianDuCaiShuiFaGui/108_',100,199))
        # small test
        # data.extend(data)
        threadLock.acquire()
        datalist.extend(data)

        threadLock.release()
        print(data)
        print("退出线程：" + self.name)

class Thread_Center6(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("开始线程：" + self.name)
        # print_time(self.name, self.counter, 5)
        data = (Generator_Shui5.GetMultPages('https://www.shui5.cn/article/NianDuCaiShuiFaGui/108_',1,99))
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
        data = (Generator_Shui5.GetMultPages('https://www.shui5.cn/article/DiFangCaiShuiFaGui/145_',700,962))
        # small test
        # data.extend(data)
        threadLock.acquire()  # lock

        datalist.extend(data)

        threadLock.release()
        print(data)
        print("退出线程：" + self.name)

class Thread_Loc2(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("开始线程：" + self.name)
        # print_time(self.name, self.counter, 5)
        data = (Generator_Shui5.GetMultPages('https://www.shui5.cn/article/DiFangCaiShuiFaGui/145_',500,699))
        # small test
        # data.extend(data)
        threadLock.acquire()  # lock

        datalist.extend(data)

        threadLock.release()
        print(data)
        print("退出线程：" + self.name)

class Thread_Loc3(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("开始线程：" + self.name)
        # print_time(self.name, self.counter, 5)
        data = (Generator_Shui5.GetMultPages('https://www.shui5.cn/article/DiFangCaiShuiFaGui/145_',300,499))
        # small test
        # data.extend(data)
        threadLock.acquire()  # lock

        datalist.extend(data)

        threadLock.release()
        print(data)
        print("退出线程：" + self.name)

class Thread_Loc4(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("开始线程：" + self.name)
        # print_time(self.name, self.counter, 5)
        data = (Generator_Shui5.GetMultPages('https://www.shui5.cn/article/DiFangCaiShuiFaGui/145_',100,299))
        # small test
        # data.extend(data)
        threadLock.acquire()  # lock

        datalist.extend(data)

        threadLock.release()
        print(data)
        print("退出线程：" + self.name)

class Thread_Loc5(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("开始线程：" + self.name)
        # print_time(self.name, self.counter, 5)
        data = (Generator_Shui5.GetMultPages('https://www.shui5.cn/article/DiFangCaiShuiFaGui/145_',1,99))
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
    thread1=Thread_Center1(1,'C1',1)
    thread2=Thread_Center2(2,'C2',2)
    thread3=Thread_Center3(3,'C3',3)
    thread4=Thread_Center4(4,'C4',4)
    thread5=Thread_Center5(5,'C5',5)
    thread6=Thread_Center6(6,'C6',6)
    thread7=Thread_Loc1(7,'L1',7)
    thread8=Thread_Loc2(8,'L2',8)
    thread9=Thread_Loc3(9,'L3',9)
    thread10=Thread_Loc4(10,'L4',10)
    thread11=Thread_Loc5(11,'L5',11)

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()
    thread6.start()
    thread7.start()
    thread8.start()
    thread9.start()
    thread10.start()
    thread11.start()
    # threads.append(thread1)
    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
    thread5.join()
    thread6.join()
    thread7.join()
    thread8.join()
    thread9.join()
    thread10.join()
    thread11.join()

    print('All thread off')
    print(datalist)
    DataModel.IntoSqlite(datalist)
