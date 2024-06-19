#!/usr/bin/env python3
"""
Caching request module
"""
import redis
import requests
from functools import wraps
from typing import Callable

# Initialize Redis client globally
client = redis.Redis()

def track_get_page(fn: Callable) -> Callable:
    """ Decorator for get_page """
    @wraps(fn)
    def wrapper(url: str) -> str:
        """ Wrapper that:
            - Checks whether a URL's data is cached
            - Tracks how many times get_page is called
        """
        # Increment the count of accesses
        client.incr(f'count:{url}')
        
        # Check if the page is cached
        cached_page = client.get(f'{url}')
        if cached_page:
            return cached_page.decode('utf-8')
        
        # Fetch the page content if not cached
        response = fn(url)
        
        # Cache the content with an expiry of 10 seconds
        client.setex(f'{url}', 10, response)
        
        return response
    return wrapper

@track_get_page
def get_page(url: str) -> str:
    """ Makes a HTTP request to a given endpoint """
    response = requests.get(url)
    return response.text

# Example usage
if __name__ == "__main__":
    test_url = "http://slowwly.robertomurray.co.uk"
    print(get_page(test_url))
    print(get_page(test_url))
    
    # Check access count
    print(f"Access count: {client.get(f'count:{test_url}').decode('utf-8')}")
