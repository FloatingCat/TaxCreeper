import redis

from src.Model.Redis_connecter import RedisConn
from src.controller.config import redis_config


def url_put(index_1=30, index_2=30):
    r = RedisConn().r
    r.set('food', 'mutton', ex=3)  # key是"food" value是"mutton" 将键值对存入redis缓存
    print(r.get('food'))  # mutton 取出键food对应的值
    print(r.time())
    pipe = r.pipeline()
    for i in range(1, index_1):  # 602
        pipe.sadd('waiting_url', 'https://www.shui5.cn/article/NianDuCaiShuiFaGui/108_' + str(i) + '.html')
    for i in range(1, index_2):  # 962
        pipe.sadd('waiting_url', 'https://www.shui5.cn/article/DiFangCaiShuiFaGui/145_' + str(i) + '.html')
    pipe.execute()
    r.sunionstore('val_url', 'waiting_url')
    print(r.scard('waiting_url'))
    r.close()


if __name__ == '__main__':
    url_put()
