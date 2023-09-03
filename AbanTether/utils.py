import redis

rds = redis.Redis(host='localhost', port=6379, db=0)


def get_count(key):
    try:
        count = int(rds.get(key))
    except TypeError:
        count = 0
    return count


def count_plus_one(key):
    count = get_count(key)
    rds.set(key, count+1)
