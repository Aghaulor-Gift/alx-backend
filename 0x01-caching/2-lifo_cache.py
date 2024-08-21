#!/usr/bin/env python3
"""LIFO module that Create a class LIFOCache that inherits from BaseCaching
and is a caching system."""
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """A LIFO class that inherits from BaseCaching and
    implements a LIFO caching system"""
    def __init__(self):
        """Inherit the initialisation from the parent class"""
        super().__init__()
        self.lifo_list = []

    def put(self, key, item):
        """A method that add item to the cache using the key"""
        if key is None or item is None:
            return

        self.cache_data[key] = item
        self.lifo_list.append(key)

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            last_key = self.lifo_list.pop(-2)
            del self.cache_data[last_key]
            print(f'DISCARD: {last_key}')

    def get(self, key):
        """Retrieve an item by key from the cache."""
        return self.cache_data.get(key, None)
