from redis_record import set_mission_status
from databus.internal.dao.kafka_producer import get_producer_ins

kfk = get_producer_ins(None)


def create_mission(url: str):
    # kafka投递
    kfk.send('tax_crawler', 'mission_seq', url, 0)
    # redis日志记录
    set_mission_status(page_url=url, status="seq")


def receive_mission_result(url: str, status_code: str):
    # redis日志记录回写
    set_mission_status(page_url=url, status=status_code)
