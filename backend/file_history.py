import redis

def lrange(key, start, stop):
    r = redis.Redis(host='localhost', port=6379, db=0)
    vals = r.lrange(key, start, stop)
    r.quit()
    return vals

def lpush(key, value):
    r = redis.Redis(host='localhost', port=6379, db=0)
    val = r.lpush(key, value)
    r.quit()
    return val

def lpushes(key, *values):
    r = redis.Redis(host='localhost', port=6379, db=0)
    vals = r.lpush(key, values)
    r.quit()
    return vals

def rpop(key):
    r = redis.Redis(host='localhost', port=6379, db=0)
    val = r.rpop(key)
    r.quit()
    return val

#Returns an array of popped values or nil
def rpops(key, n):
    r = redis.Redis(host='localhost', port=6379, db=0)
    vals = r.rpop(key, n)
    r.quit()
    return vals