from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import kafka_errors
from typing import Optional, List
import traceback
import json
import threading


# 线程安全单例
def synchronized(func):
    func.__lock__ = threading.Lock()

    def synced_func(*args, **kws):
        with func.__lock__:
            return func(*args, **kws)

    return synced_func


def Singleton(cls):
    instances = {}

    @synchronized
    def get_instance(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return get_instance


@Singleton
class KafkaProducerIns:
    def __init__(self, bootstrap_servers=None):
        if bootstrap_servers is None:
            bootstrap_servers = ['localhost:9092']
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            key_serializer=lambda k: json.dumps(k).encode(),
            value_serializer=lambda v: json.dumps(v).encode())

    def send(self, topic, key, value, partition: Optional[int]):
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
