from databus.internal.model.kafka_instance import get_producer_ins, _KafkaConsumer
from databus.internal.utils.log import LOGGER


def test_producer():
    ts = get_producer_ins(None)
    su_list = []
    # 发送三条消息
    for i in range(1, 3):
        print(i)
        res = ts.post_mission('kafka_demo', str(i), str(i), 0)
        su_list.append(res)

    print(su_list)


def test_consumer():
    ts = _KafkaConsumer("kafka_demo")
    resp = ts.get_mission()
    LOGGER.info(resp)
