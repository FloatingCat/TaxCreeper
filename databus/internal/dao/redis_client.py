import redis
from databus.internal.configs import redis_config
from databus.internal.utils.singleton.singleton import Singleton


def get_redis_conn():
    return RedisConn().r


@Singleton
class RedisConn:
    def __init__(self):
        self.pool = redis.ConnectionPool(host=redis_config['host'], port=redis_config['port'],
                                         decode_responses=redis_config['decode_responses'],
                                         )
        self.r = redis.Redis(connection_pool=self.pool)
