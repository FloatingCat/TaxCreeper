#  Redis相关操作，逻辑层
from databus.internal.model.redis_client import get_redis_conn

__redis_cli = get_redis_conn()


# 考虑一个问题，当新任务发出，但是Redis日志队列中仍然有重复的URL任务时，Kafka中的任务已经发出了，对redis任务做更改是无意义的，所以应该允许URL重复，用唯一ID做标识

def add_mission_status(page_url: str, latest_post: float):
    """

    :param page_url:
    :param latest_post:
    :return:
    """
    return __redis_cli.hset("missions", page_url, latest_post)


def remove_mission_status(page_url, latest_receive: float):
    """

    :param page_url: 查验url
    :param latest_receive:时间戳校验
    :return:
    """
    if __redis_cli.hget("missions", page_url) == str(latest_receive):  # 但是读出来的是个str
        return __redis_cli.hdel("missions", page_url)
    else:

        return
