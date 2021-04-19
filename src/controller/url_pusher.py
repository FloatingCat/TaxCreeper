import redis
def url_put():
    pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
    r = redis.Redis(connection_pool=pool)
    r.set('food', 'mutton', ex=3)  # key是"food" value是"mutton" 将键值对存入redis缓存
    print(r.get('food'))  # mutton 取出键food对应的值
    print(r.time())
    for i in range(1, 20):#602
        r.sadd('waiting_url','https://www.shui5.cn/article/NianDuCaiShuiFaGui/108_' + str(i)+'.html')
    for i in range(1, 30):#962
        r.sadd('waiting_url','https://www.shui5.cn/article/DiFangCaiShuiFaGui/145_' + str(i)+'.html')
    print(r.scard('waiting_url'))
    r.close()
if __name__=='__main__':
    url_put()