#  Redis相关操作，逻辑层
from databus.internal.model.redis_client import get_redis_conn

__redis_cli = get_redis_conn()


# 考虑一个问题，当新任务发出，但是Redis日志队列中仍然有重复的URL任务时，Kafka中的任务已经发出了，对redis任务做更改是无意义的，所以应该允许URL重复，用唯一ID做标识

def set_mission_status(topic: str, mission_content: str, latest_post: float):
    """

    :param topic:
    :param mission_content:
    :param latest_post:
    :return:
    """
    return __redis_cli.hset(topic, mission_content, latest_post)


def get_all_mission(topic: str) -> dict:
    """

    :return:
    """
    resp = __redis_cli.hgetall(topic)
    if resp:
        return resp
    else:
        return dict()


def remove_mission_status(topic: str, mission_content, latest_receive: float) -> dict:
    """

    :param topic:
    :param mission_content:
    :param latest_receive:
    :return:
    """
    # 检测到队列中有对应条目，且时间戳一致才能删除，否则就让他自然死亡
    if __redis_cli.hget(topic, mission_content) == str(latest_receive):  # 但是读出来的是个str
        return {
            "status": "ok",
            "content": __redis_cli.hdel(topic, mission_content)
        }
    else:
        return {"status": "not_found", }


def set_dead_mission(topic: str, mission_content: str, latest_post: float):
    rm_status = remove_mission_status(topic, mission_content, latest_post)
    if rm_status["status"] == "not_found":
        return rm_status
    else:
        return {
            "status": "ok",
            "content": __redis_cli.hset(topic + "_dead", mission_content, latest_post)
        }


def get_all_dead_mission(topic: str) -> dict:
    resp = __redis_cli.hgetall(topic + "_dead")
    if resp:
        return resp
    else:
        return dict()
