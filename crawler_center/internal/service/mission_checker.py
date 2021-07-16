from crawler_center.internal.dao.sql_record import create_record_sql
from crawler_center.internal.dao.sql_result import create_result_sql
from crawler_center.configs.configs import srv_hosts
import requests


def process_mission_result(arrival_result:dict):
    if arrival_result["status"] != "ok": #从端异常任务
        create_record_sql()
        requests.post(url=srv_hosts["databus"]+"/check_mission/", data=None)
    else: # 从端成功任务
        create_record_sql()
        requests.post(url=srv_hosts["databus"]+"/check_mission/", data=None)