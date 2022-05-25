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

# Store history of functions applied to dataframe
# key   = filename + _h --- EX: test.csv_h
# value = 'some_string_with_information_about_function_and_arguments' 
def lpush(key, value, df):
    key = key + '_h'
    r = g.redis
    g.current_function['name'] = get_function_name(value)
    val = r.lpush(key, value)
    key = key + '_df'
    update_df(key, df)
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

def update_df(key, df):
    r = g.redis
    df_compressed = pa.serialize(df).to_buffer().to_pybytes()
    r.set(key, df_compressed)

# Input  -> replace_na_mode_numeric:temperature 
# Return -> replace_na_mode_numeric
def get_function_name(value):
    return value.split(':')[0]