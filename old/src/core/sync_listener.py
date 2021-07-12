# 检测到Redis爬取队列空且Redis校验队列不为空时将校验队列拷贝至爬取队列
from old.src.Model.Redis_connecter import RedisConn


def sync_listener():
    r = RedisConn().r
    if r.scard('waiting_url') == 0 and r.scard('val_url') != 0:
        r.sunionstore('waiting_url', 'val_url')
