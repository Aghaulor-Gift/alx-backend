#!/usr/bin/env python3
"""Most Recently Used(MRU) module that create a class MRUCache that inherits
from BaseCaching and is a caching system"""
from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """A MRU class that implements the MRU algorithm"""
    def __init__(self):
        """ Inherit initialisation from parent class"""
        super().__init__()
        self.mru_list = []

    def put(self, key, item):
        """Add item by key to the cache"""
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.mru_list.remove(key)
        self.cache_data[key] = item
        self.mru_list.append(key)

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            recent_key = self.mru_list.pop(0)
            del self.cache_data[recent_key]
            print(f"DISCARD: {recent_key}")

    def get(self, key):
        """Retrieve the recent item by key in the cache"""
        return self.cache_data.get(key, None)
