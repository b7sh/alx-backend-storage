#!/usr/bin/env python3
'''Implementing an expiring web cache and tracker'''
import redis
import requests
from functools import wraps


redis_client = redis.Redis()


def access(method):
    '''Decorator for get_page to track URL access and caching.'''
    @wraps(method)
    def count(url: str) -> str:
        '''Track how many times a particular URL was accessed.'''
        cached = redis_client.get(f'cached:{url}')
        if cached:
            redis_client.incr(f'count:{url}')
            return cached.decode('utf-8')
        res = method(url)
        redis_client.setex(f'cached:{url}', 10, res)
        redis_client.incr(f'count:{url}')
        return res
    return count


@access
def get_page(url: str) -> str:
    '''Send request to the URL.'''
    return requests.get(url).text


if __name__ == '__main__':
    get_page(
            '''http://slowwly.robertomurray.co.uk/delay/5000/url/
            http://www.google.com''')
