import datetime
import json
import time
from hashlib import md5

from redis_record import add_mission_status
from databus.internal.dao.kafka_producer import get_producer_ins

kfk = get_producer_ins(None)


def create_mission(url: str):
    """

    :param url: 页面链接，任务唯一标识
    :return:
    """
    post_time = time.time()
    # kafka投递
    kfk.send('tax_crawler', 'mission_seq', json.dumps({"url": url, "post_time": post_time}), 0)
    # redis日志记录
    add_mission_status(page_url=url, latest_post=post_time)


def receive_mission_result(url: str, status_code: str):
    """

    :param url:
    :param status_code: 任务处理最终状态
    :return: redis日志记录回写
    """

    add_mission_status(page_url=url, status=status_code)
