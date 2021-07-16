import time

from crawler_center.internal.model.sql_client import get_session, MissionResult


def create_result_sql(url: str, mission_time: float, finish_time: float, topic: str, location: str, postdate: str,
                      content: str, file_links):
    with get_session() as ds:
        mr = MissionResult(url=url, mission_time=mission_time, finish_time=finish_time,
                           topic=topic, location=location, postdate=postdate, content=content, file_links=file_links)
        ds.add(mr)
        ds.commit()


if __name__ == "__main__":
    create_result_sql("111.com", time.time(), time.time() + 1000, "tts", "CN", "test_date", "tst___", "")
