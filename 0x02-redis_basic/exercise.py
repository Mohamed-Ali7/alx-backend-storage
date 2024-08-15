#!/usr/bin/env python3
"""This module contains Cache class"""

from functools import wraps
from typing import Any, Callable, Union
import redis
import uuid


def count_calls(method: Callable) -> Callable:
    """Tracks the number of calls made to a method in a Cache class"""
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """returns the given method after incrementing its call counter."""

        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    """Represents a caching object to store data in Redis"""

    def __init__(self) -> None:
        """Initialize an instance of the class"""
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @count_calls
    def store(self, data:  Union[str, bytes, int, float]) -> str:
        """Stores a value in the cache"""
        data_key = str(uuid.uuid4())
        self._redis.set(data_key, data)
        return data_key

    def get(self, key: str, fn: Callable = None,
            ) -> Union[str, bytes, int, float]:
        """Retrieves a value from the cache"""
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        """Retrieves a string value from the cache"""
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """Retrieves an integer value from the cache"""

        return self.get(key, lambda x: int(x))
