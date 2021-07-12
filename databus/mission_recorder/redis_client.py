import redis
from databus.configs import redis_config
from databus.singleton.singleton import Singleton


@Singleton
class RedisConn:
    def __init__(self):
        self.pool = redis.ConnectionPool(host=redis_config['host'], port=redis_config['port'],
                                         decode_responses=redis_config['decode_responses'],
                                         password=redis_config['password'])
        self.r = redis.Redis(connection_pool=self.pool)
