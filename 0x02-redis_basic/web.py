#!/usr/bin/env python3
"""
mod doc
"""


import redis
import requests
from typing import Callable
from functools import wraps

# Initialize Redis client
r = redis.Redis()


def cache_with_expiry(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(url: str) -> str:
        # Generate cache keys
        count_key = f"count:{url}"
        cache_key = f"cached:{url}"

        # Increment the access count
        r.incr(count_key)

        # Check if the content is cached
        cached_content = r.get(cache_key)
        if cached_content:
            return cached_content.decode('utf-8')

        # Fetch the page content
        content = method(url)

        # Cache the content with an expiry of 10 seconds
        r.setex(cache_key, 10, content)

        return content
    return wrapper


@cache_with_expiry
def get_page(url: str) -> str:
    response = requests.get(url)
    return response.text


# Testing the functionality
if __name__ == "__main__":
    test_url = "http://slowwly.robertomurray.co.uk"
    print(get_page(test_url))
    print(get_page(test_url))

    # Check access count
    print(f"Access count: {r.get(f'count:{test_url}').decode('utf-8')}")
