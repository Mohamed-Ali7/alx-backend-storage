#!/usr/bin/env python3
"""This module contains data_cacher() and get_page() functions"""
import redis
import requests
from functools import wraps
from typing import Callable


redis_store = redis.Redis()


def data_cacher(method: Callable) -> Callable:
    """
    uses the requests module to obtain the HTML
    content of a particular URL and returns it.
    """
    @wraps(method)
    def wrapper(url) -> str:
        """The wrapper function for caching the output"""

        client = redis.Redis()
        client.incr(f'count:{url}')
        cached_page = client.get(f'{url}')
        if cached_page:
            return cached_page.decode('utf-8')
        response = method(url)
        client.set(f'{url}', response, 10)
        return response
    return wrapper


@data_cacher
def get_page(url: str) -> str:
    """
    Tracks how many times a particular URL was accessed in the key
    "count:{url}" and cache the result with an expiration time of 10 seconds.
    """
    return requests.get(url).text
