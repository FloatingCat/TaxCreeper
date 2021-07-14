import json
import traceback
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import kafka_errors
from typing import Optional
from databus.internal.utils.singleton.singleton import Singleton
from databus.internal.utils.log import LOGGER


@Singleton
class _KafkaProducer:
    def __init__(self, bootstrap_servers=None):
        LOGGER.info("Create a KafkaProducer at " + str(bootstrap_servers))
        if bootstrap_servers is None:
            bootstrap_servers = ['localhost:9092']
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            key_serializer=lambda k: json.dumps(k).encode(),
            value_serializer=lambda v: json.dumps(v).encode())

    def post_mission(self, topic, key, value, partition: Optional[int]):
        future = self.producer.send(
            topic=topic,
            key=key,  # 同一个key值，会被送至同一个分区
            value=value,
            partition=partition)  # 向分区1发送消息
        # print(value)
        try:
            future.get(timeout=10)  # 监控是否发送成功
            return True
        except kafka_errors:  # 发送失败抛出kafka_errors
            traceback.format_exc()
            return False


def get_producer_ins(_bootstrap_servers: None):
    ins = _KafkaProducer(_bootstrap_servers)
    return ins


# 每一个连接看做一个消费者，这个思路是对的
class _KafkaConsumer:
    def __init__(self, topic: str, group_id: str, bootstrap_servers=None, ):
        LOGGER.info("New consumer for " + topic)
        if bootstrap_servers is None:
            bootstrap_servers = ['localhost:9092']
        self.consumer = KafkaConsumer(
            topic,
            group_id=group_id,
            bootstrap_servers=bootstrap_servers,
            auto_offset_reset='latest',
            key_deserializer=lambda k: json.loads(k.decode()),
            value_deserializer=lambda v: json.loads(v.decode()))

    def get_mission(self):
        try:
            LOGGER.info("Polling a mission...")
            future = self.consumer.poll(max_records=1,update_offsets=False)  # 监控是否成功
            print(future)
            return future
        except kafka_errors:  # 发送失败抛出kafka_errors
            traceback.format_exc()
            return False

    # def __del__(self):
    #     self.consumer.close()
# def get_producer_ins(_bootstrap_servers: None):
#     ins = _KafkaProducer(_bootstrap_servers)
#     return ins
