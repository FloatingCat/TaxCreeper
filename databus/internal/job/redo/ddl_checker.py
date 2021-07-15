# job，检查过期任务，根据配置定时执行
import time

from databus.internal.dao.record.redis_record import get_all_mission, set_dead_mission
from databus.internal.service.poster.mission_create import create_mission
from databus.internal.utils.log import LOGGER
__time_range = 30  # 超时600s
__mission_topic = ['tax_crawler']


def checker() -> dict:
    """
    job，检查过期任务
    :return:
    """
    LOGGER.info("checking TTL...")
    for topic in __mission_topic:
        all_missions = get_all_mission(topic)

        if not all_missions:
            LOGGER.info("all mission finished")
            return {"status": "all_mission_finish", "length": 0}
        else:
            LOGGER.info("remain missions: "+str(all_missions))
            now_time = time.time()
            for k, v in all_missions.items():
                if now_time - float(v) > __time_range:
                    LOGGER.info("found TTL overtime! in "+str(k)+" : "+str(v))
                    set_dead_mission(topic, k, v)
                    create_mission(topic, k)
            return {"status": "remain", "length": len(all_missions)}
