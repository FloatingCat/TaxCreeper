from databus.internal.dao.record.redis_record import set_mission_status
from logging import Logger


def test_conn():
    resp = str(set_mission_status("tax_crawler","111", 11.11))
    logger = Logger("test")
    print(resp)
    logger.info(resp)
