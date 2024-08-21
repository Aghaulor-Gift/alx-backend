#!/usr/bin/env python3
""" Basic cache module with class BasicCache that inherits from BaseCaching
and is a caching system.
"""
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """A class that inherits from BaseCaching"""
    def put(self, key, item):
        """Method to add items to the cache using the key"""
        if key is None or item is None:
            return
        self.cache_data[key] = item

    def get(self, key):
        """ A method that get the item by using the key"""
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data.get(key)
