from databus.internal.dao.record.redis_record import get_all_dead_mission
from databus.internal.dao.record.redis_record import remove_mission_status


# TODO:删除dead_seq
def mission_check(topic: str, url: str, latest_receive: float) -> dict:
    res_dict = {}
    all_walking_dead = get_all_dead_mission(topic)
    remove_res = remove_mission_status(topic, url, latest_receive)
    res_dict.update({"ttl_dead_seq": all_walking_dead, "ttl_removed": remove_res})
    return res_dict
