#!/usr/bin/env python3
""" Least Frequently Used(LFU) module that Create a class LFUCache that
inherits from BaseCaching and is a caching system"""
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """ LFU class that inherits from BaseCaching to implement LFU algorithm"""
    def __init__(self):
        """ Inherit from the parent class"""
        super().__init__()
        self.lfu_list = []

    def put(self, key, item):
        """ Add item by key in the cache"""
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.lfu_list.remove(key)
        self.cache_data[key] = item
        self.lfu_list.append(key)

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            least_frequent_key = self.lfu_list.pop(0)
            del self.cache_data[least_frequent_key]
            print(f'DISCARD: {least_frequent_key}')

    def get(self, key):
        """ Retrieve item by key from the cache"""
        return self.cache_data.get(key)
