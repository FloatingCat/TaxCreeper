import uvicorn
import time
import random
from multiprocessing import Process

from databus.internal.server.http_srv import app
from databus.internal.job.redo.ddl_checker import checker

# zookeeper-server-start -daemon /usr/local/etc/kafka/zookeeper.properties & kafka-server-start /usr/local/etc/kafka/server.properties


def databus_run():
    uvicorn.run(app, host="0.0.0.0", port=10005, reload=False)


def refresh_job():
    while True:
        checker()
        time.sleep(10)


if __name__ == "__main__":
    db_main = Process(target=databus_run)
    job = Process(target=refresh_job)
    db_main.start()
    job.start()
    db_main.join()
    job.join()
