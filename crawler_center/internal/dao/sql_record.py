import time

from crawler_center.internal.model.sql_client import get_session, MissionRecord


def create_record_sql(page_url: str, mission_time: float, finish_time: float, mission_status: str, poster: str, carrier: str):
    with get_session() as ds:
        mr = MissionRecord(page_url=page_url, mission_time=mission_time, finish_time=finish_time,
                           mission_status=mission_status, poster=poster, carrier=carrier)
        ds.add(mr)
        ds.commit()


if __name__ == "__main__":
    create_record_sql("111.com", time.time(), time.time()+200, "fin", "py-tester", "container-0")
