
from redis import Redis, ConnectionPool
from fastapi import HTTPException
from src.config import redis_setting


def redis_client(db:int = 0):
    try:
        pool = ConnectionPool(max_connections=10, host=redis_setting.redis_host, port=int(redis_setting.redis_port),db=db)
        red = Redis(connection_pool=pool, db=db)
        print(red)
        return red
    except:
        raise HTTPException(status_code=500, detail="Redis Cant Connect")