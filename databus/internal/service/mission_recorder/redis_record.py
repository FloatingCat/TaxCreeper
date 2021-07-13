from databus.internal.dao.redis_client import get_redis_conn

__redis_cli = get_redis_conn()


def set_mission_status(page_url: str, status: str):
    return __redis_cli.hset("missions", page_url, status)
