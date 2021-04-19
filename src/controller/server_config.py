# settings for connecting redis-server
import redis


def connect_redis_server():
    pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
    r = redis.Redis(connection_pool=pool)
    r.set('food', 'mutton', ex=3)  # key是"food" value是"mutton" 将键值对存入redis缓存
    print(r.get('food'))  # mutton 取出键food对应的值
    print(r.time())
    return r
if __name__=='__main__':
    connect_redis_server()



