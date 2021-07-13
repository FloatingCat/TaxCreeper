import datetime
import time
from hashlib import md5
from uuid import uuid4


def gen_uid4():
    return uuid4().hex


if __name__ == "__main__":
    # print((gen_uid4()+str(datetime.datetime.now().strftime("_%Y%m%d_%H%M%S_%f"))))
    print(len(md5("111".encode("utf-8")).hexdigest()+str(datetime.datetime.now().strftime("_%Y%m%d_%H%M%S_%f"))))
    print(time.time(),type(time.time()))