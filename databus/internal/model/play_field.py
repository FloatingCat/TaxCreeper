from databus.internal.model.redis_client import get_redis_conn

__redis_cli = get_redis_conn()

if __name__ == "__main__":
    resp = __redis_cli.hget("missions","111")
    print(resp, type(resp))
    print(__redis_cli.hdel("missions","111"))