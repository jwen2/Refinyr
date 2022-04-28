import redis
import pyarrow as pa
from flask import g

def get_datastore():
    if ('redis' not in g):
        g.redis = redis.Redis(host='localhost', port=6379, db=0)
    return g.redis 

def close_datastore():
    redis_connection = g.pop('redis', None)
    if (redis_connection is not None):
        redis_connection.quit()

def lrange(key, start, stop):
    key = key + '_h'
    r = g.redis
    vals = r.lrange(key, start, stop)
    return vals

def lpush(key, value):
    key = key + '_h'
    r = g.redis
    val = r.lpush(key, value)
    return val

def lpushes(key, *values):
    key = key + '_h'
    r = g.redis
    vals = r.lpush(key, values)
    return vals

def rpop(key):
    key = key + '_h'
    r = g.redis
    val = r.rpop(key)
    return val

#Returns an array of popped values or nil
def rpops(key, n):
    key = key + '_h'
    r = g.redis
    vals = r.rpop(key, n)
    return vals

def store_df(key, df):
    key = key + '_df'
    r = g.redis
    df_compressed = pa.serialize(df).to_buffer().to_pybytes()
    res = r.set(key,df_compressed)

def get_df(key):
    key = key + '_df'
    r = g.redis
    data = r.get(key)
    try:
        return pa.deserialize(data)
    except:
        print("No data")