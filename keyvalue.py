import redis
import ujson as json
import os
import functools

@functools.lru_cache(maxsize=100)
def get_key(key):
    return STORE._get(key)


class RedisKV:
    def __init__(self):
        print("Using redis KV store")
        self.conn = redis.Redis.from_url(os.environ['REDIS_URL'])

    def exists(self, key):
        assert isinstance(key, str), "keys must be str"
        return self.conn.exists(key) == 1


    def _get(self, key):
        assert isinstance(key, str), "keys must be str"
        value = self.conn.get(key)
        if value is None:
            raise ValueError("couldn't find {} in store".format(key))
        return json.loads(value, precise_float=True)


    def get(self, key):
        return get_key(key)


    def set(self, key, value):
        assert isinstance(key, str), "keys must be str"
        value_json = json.dumps(value, double_precision=16)
        self.conn.set(key, value_json)


    def delete(self, key):
        assert isinstance(key, str), "keys must be str"
        self.conn.delete(key)


    def refcount_incr(self, key):
        assert isinstance(key, str), "keys must be str"
        key = "counter:" + key
        return self.conn.incr(key)


    def refcount_decr(self, key):
        assert isinstance(key, str), "keys must be str"
        key = "counter:" + key
        result = self.conn.decr(key)
        if result == 0:
            self.conn.delete(key)
        return result


class LocalKV:
    def __init__(self):
        print("Using in-memory KV store")
        self.backing_store = {}

    def exists(self, key):
        assert isinstance(key, str), "keys must be str"
        return key in self.backing_store


    def _get(self, key):
        assert isinstance(key, str), "keys must be str"
        if key not in self.backing_store:
            raise ValueError("couldn't find {} in store".format(key))
        return json.loads(self.backing_store[key], precise_float=True)


    def get(self, key):
        return get_key(key)


    def set(self, key, value):
        assert isinstance(key, str), "keys must be str"
        value_json = json.dumps(value, double_precision=16)
        self.backing_store[key] = value_json

    def delete(self, key):
        assert isinstance(key, str), "keys must be str"
        del self.backing_store[key]


    def refcount_incr(self, key):
        assert isinstance(key, str), "keys must be str"
        key = "counter:" + key

        self.backing_store[key] = self.backing_store.get(key, 0) + 1
        return self.backing_store[key]

    def refcount_decr(self, key):
        assert isinstance(key, str), "keys must be str"
        key = "counter:" + key
        if key not in self.backing_store:
            raise ValueError("couldn't find {} in store".format(key))

        result = self.backing_store[key] - 1
        self.backing_store[key] = result
        if result == 0:
            del self.backing_store[key]
        return result


if os.environ.get('PRODUCTION') is not None:
    STORE = RedisKV()
else:
    STORE = LocalKV()
