from databus.internal.dao.record.redis_record import add_mission_status
from logging import Logger


def test_conn():
    resp = str(add_mission_status("111", 11.11))
    logger = Logger("test")
    print(resp)
    logger.info(resp)
