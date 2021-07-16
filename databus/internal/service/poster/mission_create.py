import json
import time

from databus.internal.dao.record.redis_record import set_mission_status
from databus.internal.model.kafka_instance import get_producer_ins

kfk = get_producer_ins(None)  # 我猜之后我也不会改用其他队列中间件，就别依赖注入了


def create_mission(topic: str, mission_content: str):
    post_time = time.time()
    # kafka投递
    kfk_res = kfk.post_mission(topic, 'mission_seq',
                               json.dumps({"mission_content": mission_content, "post_time": post_time}), 0)  # 向kafka投递的是json字符串，任务内容字段也是
    # redis日志记录
    rds_res = set_mission_status(topic, mission_content=mission_content, latest_post=post_time)
    res = {"status": "", "post_time": post_time}
    if kfk_res is not None and rds_res is not None:
        res["status"] = True
    else:
        res["status"] = False
    return res
