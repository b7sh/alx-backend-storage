#!/usr/bin/env python3
''' Implementing an expiring web cache and tracker '''
import redis
import requests
from functools import wraps
import hashlib


r = redis.Redis()


def generate_redis_key(url: str) -> str:
    ''' generate the key '''
    return hashlib.md5(url.encode()).hexdigest()


def cache_page(func):
    ''' track '''
    @wraps(func)
    def wrapper(url: str):
        ''' the wrapper fuction '''
        redis_key = generate_redis_key(url)
        cached_content = r.get(f"cached:{redis_key}")
        if cached_content:
            return cached_content.decode('utf-8')

        result = func(url)

        r.setex(f"cached:{redis_key}", 10, result)

        r.incr(f"count:{redis_key}")

        return result
    return wrapper


@cache_page
def get_page(url: str) -> str:
    '''
    uses the requests module to obtain
    the HTML content of a particular URL and returns it.
    '''
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        return f"Error fetching the page: {e}"


if __name__ == "__main__":
    get_page(
        '''http://slowwly.robertomurray.co.uk/
        delay/5000/url/http://www.google.com'''
        )
