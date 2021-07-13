from databus.internal.service.mission_recorder.redis_record import set_mission_status
from logging import Logger


def test_conn():
    resp = str(set_mission_status("111", "undo"))
    logger = Logger("test")
    print(resp)
    logger.info(resp)
