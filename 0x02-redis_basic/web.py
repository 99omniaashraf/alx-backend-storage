#!/usr/bin/env python3
"""
Caching request module
"""

import requests
import redis
from functools import wraps
from typing import Callable

# Initialize Redis connection
redis_client = redis.Redis()


def cache_response(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(url: str) -> str:
        cache_key = f"cache:{url}"
        cached_response = redis_client.get(cache_key)
        if cached_response:
            return cached_response.decode('utf-8')

        response = func(url)
        redis_client.setex(cache_key, 10, response)
        return response

    return wrapper


def track_access(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(url: str) -> str:
        count_key = f"count:{url}"
        redis_client.incr(count_key)
        return func(url)

    return wrapper


@cache_response
@track_access
def get_page(url: str) -> str:
    response = requests.get(url)
    return response.text
