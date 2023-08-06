from datetime import timedelta, datetime

from redis import Redis


class Cache:
    def __init__(self, cache_interval):
        self.cache_interval = cache_interval

    def exists(self, path):
        return True

    def get(self, path):
        return None

    def set(self, path, content):
        pass


class MemoryCache(Cache):
    def __init__(self, cache_interval):
        self.cache = {}
        super(MemoryCache, self).__init__(cache_interval)

    def exists(self, path):
        self.__check_timer__(path)
        return path in self.cache

    def get(self, path):
        self.__check_timer__(path)
        return self.cache[path][0]

    def set(self, path, content):
        self.cache[path] = (content, datetime.now())

    def __check_timer__(self, path):
        if path in self.cache and self.cache[path][1] + timedelta(seconds=self.cache_interval) < datetime.now():
            del self.cache[path]


class RedisCache(Cache):
    def __init__(self, cache_interval, cache_prefix, **redis_conn):
        self.redis = Redis(**redis_conn)
        self.cache_prefix = cache_prefix
        super().__init__(cache_interval)

    def exists(self, path):
        return self.redis.exists(self.cache_prefix + path)

    def get(self, path):
        return self.redis.get(self.cache_prefix + path)

    def set(self, path, content):
        self.redis.setex(name=self.cache_prefix + path, value=content, time=self.cache_interval)
