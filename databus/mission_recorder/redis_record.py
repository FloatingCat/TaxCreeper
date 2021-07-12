import redis
from uuid import uuid4


def init_mission(redis_cli: redis.client.Redis, page_url):
    """

    :param redis_cli: 客户端实例
    :param page_url: key为url
    :return:
    """
    unique_id = uuid4().hex
    return redis_cli.hset("missions_undo", page_url, unique_id)
