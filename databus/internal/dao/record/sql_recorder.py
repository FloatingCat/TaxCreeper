from databus.internal.model.sql_client import get_session, MissionRecord


def create_result_sql():
    with get_session() as ds:
        mr = MissionRecord()
        ds.add(mr)
        ds.commit()


if __name__ == "__main__":
    create_result_sql()
