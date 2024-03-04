import redis
import os

r = redis.Redis(
    host=os.getenv('REDIS_HOST'),
    port=os.getenv('REDIS_PORT'),
    decode_responses=True
)

def store_data(key, data):
    r.hset(key, mapping=data)
        
def get_all_data(key):
    return r.hgetall(key)