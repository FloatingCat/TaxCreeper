from databus.mission_recorder.redis_client import get_redis_conn

redis_cli = get_redis_conn()


def set_mission_status(page_url: str, status: str):
    return redis_cli.hset("missions", page_url, status)
