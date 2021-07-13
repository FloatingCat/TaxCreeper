import datetime
import json
import time
from hashlib import md5

from databus.internal.dao.record.redis_record import add_mission_status
from databus.internal.model.kafka_producer import get_producer_ins

kfk = get_producer_ins(None)  # 我猜之后我也不会改用其他队列中间件，就别依赖注入了


def create_mission(url: str):
    """
    :param url: 页面链接，任务唯一标识
    :return:
    """
    post_time = time.time()
    # kafka投递
    kfk.send('tax_crawler', 'mission_seq', json.dumps({"url": url, "post_time": post_time}), 0)  # 向kafka投递的是json字符串
    # redis日志记录
    add_mission_status(page_url=url, latest_post=post_time)


