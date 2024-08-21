#!/usr/bin/python3
"""LRU Caching"""
from collections import OrderedDict
from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """class LRUCache that inherits
    from BaseCaching and is a caching system"""

    def __init__(self):
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """Must assign to the dictionary """
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                discarded_key, _ = self.cache_data.popitem(last=False)
                print(f"DISCARD: {discarded_key}")
            self.cache_data[key] = item

    def get(self, key):
        """Must return the value in self.cache_data"""
        if key is not None:
            if key in self.cache_data:
                self.cache_data.move_to_end(key)
                return self.cache_data[key]
        return None
