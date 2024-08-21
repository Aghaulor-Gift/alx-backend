#!/usr/bin/env python3
"""FIFO cache module with class FIFOCache that inherits from BaseCaching
and is a caching system that uses the FIFO algorithm."""
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """ A FIFO cache class that inherits from BaseCaching"""
    def __init__(self):
        """Initialises this class by inheriting from the parent"""
        super().__init__()
        self.fifo_list = []

    def put(self, key, item):
        """Adds item to the cache using the key"""
        if key is None or item is None:
            return
        if key in self.cache_data:
            self.fifo_list.remove(key)
        self.cache_data[key] = item
        self.fifo_list.append(key)

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            first_key = self.fifo_list.pop(0)
            del self.cache_data[first_key]
            print(f"DISCARD: {first_key}")

    def get(self, key):
        """ Get item from the cache using the key"""
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data.get(key)
