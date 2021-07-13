from sqlalchemy import Column, String, VARCHAR, FLOAT, create_engine, TEXT
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:x74rtw05@localhost:3306/tax_crawler')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)  # 天然单例


def get_session():
    return DBSession()


class MissionRecord(Base):
    # 日志表
    __tablename__ = 'mission_record'

    # 表的结构:
    page_url = Column(VARCHAR(255), nullable=False, primary_key=True)
    mission_time = Column(FLOAT, nullable=False, primary_key=True)
    mission_status = Column(VARCHAR(32), nullable=False)
    poster = Column(VARCHAR(32), nullable=True)
    carrier = Column(VARCHAR(32), nullable=True)


class MissionResult(Base):
    # 结果表
    __tablename__ = 'mission_result'

    # 表的结构:
    url = Column(VARCHAR(255), nullable=False, primary_key=True, unique=True)
    mission_time = Column(FLOAT, nullable=False)
    topic = Column(VARCHAR(255), nullable=False)
    location = Column(VARCHAR(255),nullable=True)
    content = Column(TEXT, nullable=False)
    file_links = Column(TEXT, nullable=True)

