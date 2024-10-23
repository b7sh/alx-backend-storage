#!/usr/bin/env python3
''' Implementing an expiring web cache and tracker '''
import redis
import requests
from functools import wraps
import hashlib


r = redis.Redis()


def generate_redis_key(url: str) -> str:
    return hashlib.md5(url.encode()).hexdigest()


def cache_page(func):
    @wraps(func)
    def wrapper(url: str):
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
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        return f"Error fetching the page: {e}"


if __name__ == "__main__":
    url = 'http://slowwly.robertomurray.co.uk/'

    print(get_page(url))

    print(get_page(url))

    redis_key = generate_redis_key(url)
    print(f"URL accessed {r.get(f'count:{redis_key}').decode('utf-8')} times.")
