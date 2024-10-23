#!/usr/bin/env python3
''' Redis task '''
import redis
from typing import Union
import uuid


class Cache:
    'the cache class'
    def __init__(self):
        'constructor'
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, float, int, bytes]) -> str:
        'takes a data argument and returns a string.'
        random_key = str(uuid.uuid4())
        self._redis.set(random_key, data)
        return random_key
