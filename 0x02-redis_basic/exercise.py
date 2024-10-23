#!/usr/bin/env python3
''' Redis task '''
import redis
from typing import Union, Optional, Callable
from uuid import uuid4


class Cache:
    'the cache class'
    def __init__(self):
        'constructor'
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        'takes a data argument and returns a string.'
        random_key = str(uuid4())
        self._redis.set(random_key, data)
        return random_key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        ''' Reading from redis '''
        value = self._redis.get(key)
        if fn:
            value = fn(vlue)
        return value

    def get_str(self, key: str) -> str:
        ''' parameterize a value from redis to str '''
        value = self._redis.get(key)
        return value.decode('utf-8')

    def get_int(self, key: str) -> int:
        ''' parameterize a value from redis to int '''
        value = self.redis.get(key)
        try:
            value = int(value.decode('utf-8'))
        except Exception:
            value = 0
        return value
