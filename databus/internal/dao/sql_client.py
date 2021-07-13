# 导入:
import datetime

from sqlalchemy import Column, String, VARCHAR, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from hashlib import md5

# 创建对象的基类:
Base = declarative_base()
# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:x74rtw05@localhost:3306/tax_crawler')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)


# 定义User对象:
class MissionRecord(Base):
    # 表的名字:
    __tablename__ = 'mission_record'

    # 表的结构:
    uniqueID = Column(VARCHAR(64), primary_key=True, nullable=False, unique=True)
    page_url = Column(VARCHAR(255), nullable=False)
    mission_status = Column(VARCHAR(255), nullable=False)
    carrier = Column(VARCHAR(255), nullable=True)


def get_session():
    return DBSession()


def create_record_sql(page_url: str):
    with get_session() as ds:
        mr = MissionRecord(uniqueID=(md5(page_url.encode("utf-8")).hexdigest()) + str(
            datetime.datetime.now().strftime("_%Y%m%d_%H%M%S_%f"))
                           , page_url=page_url, mission_status="pre")
        ds.add(mr)
        ds.commit()


def update_record_sql(uniqueID):
    pass


if __name__ == "__main__":
    create_record_sql("www.baidu.com")
