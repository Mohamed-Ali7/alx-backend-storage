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
    def invoker(url) -> str:
        """The wrapper function for caching the output"""

        redis_store.incr(f'count:{url}')
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_store.set(f'count:{url}', 0)
        redis_store.setex(f'result:{url}', 10, result)
        return result
    return invoker


@data_cacher
def get_page(url: str) -> str:
    """
    Tracks how many times a particular URL was accessed in the key
    "count:{url}" and cache the result with an expiration time of 10 seconds.
    """
    return requests.get(url).text
