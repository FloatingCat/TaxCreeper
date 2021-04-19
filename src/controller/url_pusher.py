import redis
from src.config import redis_config
def url_put(index_1=30,index_2=30):
    pool = redis.ConnectionPool(host=redis_config['host'], port=redis_config['port'], decode_responses=redis_config['decode_responses'],password=redis_config['password'])
    # pool = redis.ConnectionPool(host='39.97.175.209', port=6379, decode_responses=True,password='x74rtw05')
    r = redis.Redis(connection_pool=pool)
    r.set('food', 'mutton', ex=3)  # key是"food" value是"mutton" 将键值对存入redis缓存
    print(r.get('food'))  # mutton 取出键food对应的值
    print(r.time())
    for i in range(1, index_1):#602
        r.sadd('waiting_url','https://www.shui5.cn/article/NianDuCaiShuiFaGui/108_' + str(i)+'.html')
    for i in range(1, index_2):#962
        r.sadd('waiting_url','https://www.shui5.cn/article/DiFangCaiShuiFaGui/145_' + str(i)+'.html')
    print(r.scard('waiting_url'))
    r.close()
if __name__=='__main__':
    url_put()