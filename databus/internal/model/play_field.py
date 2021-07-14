import datetime
import time

from databus.internal.model.redis_client import get_redis_conn
from databus.internal.model.kafka_instance import get_producer_ins, _KafkaConsumer
from databus.internal.utils.log import LOGGER
from databus.internal.dao.record.redis_record import get_all_mission, set_mission_status, remove_mission_status

__redis_cli = get_redis_conn()


def kfk():
    ts = get_producer_ins(None)
    print(ts)
    su_list = []
    # 发送三条消息
    for i in range(1, 3):
        print(i)
        res = ts.post_mission('kafka_demo', str(i), str(i), 0)
        su_list.append(res)

    print(su_list)


def kfk_con():
    ts = _KafkaConsumer("kafka_demo", "test")
    resp = ts.get_mission()
    LOGGER.info(resp)
    print(resp)
    # for msg in consumer:
    #     recv = "%s:%d:%d: key=%s value=%s" % (msg.topic, msg.partition, msg.offset, msg.key, msg.value)
    #     print(recv)


def rd_conn():
    set_mission_status("222", 222.22)
    set_mission_status("333", 33.22)


if __name__ == "__main__":
    # kfk()
    # kfk_con()
    # resp = __redis_cli.hget("missions","111")
    # print(resp, type(resp))
    # print(__redis_cli.hdel("missions","111"))
    # rd_conn()
    # print(get_all_mission())
    # t1 = time.time()
    # time.sleep(10)
    # __time_range = time.time()-t1
    # print(__time_range)
    print(float("111.111234"))
