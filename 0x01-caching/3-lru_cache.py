#!/usr/bin/env python3
""" Least Recently Used Module that create a class LRUCache that inherits
from BaseCaching and is a caching system."""
from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """LRU class that implement LRU algorrithm"""
    def __init__(self):
        """ Inherit the initialisation from the parent class"""
        super().__init__()
        self.lru_list = []

    def put(self, key, item):
        """Add the item by the key from the cache"""
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.lru_list.remove(key)
        self.cache_data[key] = item
        self.lru_list.append(key)

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            least_key = self.lru_list.pop(0)
            del self.cache_data[least_key]
            print(f'DISCARD: {least_key}')

    def get(self, key):
        """Retrieve the item by key from the cache"""
        if key is None or key not in self.cache_data:
            return None
        self.lru_list.remove(key)
        self.lru_list.append(key)
        return self.cache_data.get(key)
