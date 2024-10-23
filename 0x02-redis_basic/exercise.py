#!/usr/bin/eenv python3
'''
Create a Cache class. In the __init__ method,
store an instance of the Redis client as
a private variable named _redis (using redis.Redis())
and flush the instance using flushdb.
Create a store method that takes a data argument
and returns a string. The method should generate
a random key (e.g. using uuid),
store the input data in Redis using
the random key and return the key.
'''
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
