#!/usr/bin/python3
"""MRU Caching"""
from collections import OrderedDict
from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """MRUCache that inherits from
    BaseCaching and is a caching system:"""

    def __init__(self):
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """Must assign to the dictionary """
        if key in self.cache_data:
            self.cache_data.move_to_end(key)
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                discarded_key = next(iter(self.cache_data.keys()))
                print(f"DISCARD: {discarded_key}")
                self.cache_data.popitem(last=False)
            self.cache_data[key] = item

    def get(self, key):
        """Must return the value in self.cache_data"""
        if key is not None:
            if key in self.cache_data:
                value = self.cache_data[key]
                self.cache_data.move_to_end(key)
                return value
        return None
