#!/usr/bin/env python3
"""FIFO caching"""

from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """FIFO caching"""

    def __init__(self):
        """Initiliaze
        """
        super().__init__()

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key and item:
            self.cache_data[key] = item
            if (len(self.cache_data) > BaseCaching.MAX_ITEMS):
                for key, _ in self.cache_data.items():
                    print(f"DISCARD: {key}")
                    break
                del self.cache_data[key]
        else:
            pass

    def get(self, key):
        """ Get an item by key
        """
        if key in self.cache_data:
            return self.cache_data[key]
        return None
