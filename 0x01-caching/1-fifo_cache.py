#!/usr/bin/env python3
"""Module implements the FIFO caching replacement
policy"""

from collections import deque

BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache(BaseCaching):
    """Implements the FIFO caching replacement
    policy"""

    def __init__(self):
        self.ordered_cache_data = list()
        super().__init__()

    def put(self, key, item):
        """Assigns value to cache"""
        if key and item:
            self.cache_data[key] = item
            if key not in self.ordered_cache_data:
                self.ordered_cache_data.append(key)

        if len(self.ordered_cache_data) > self.MAX_ITEMS:
            discarded_key = self.ordered_cache_data.pop(0)
            del self.cache_data[discarded_key]
            print(f"DISCARD: {discarded_key}")

    def get(self, key):
        """Returns a value of a particular key from
                self.cache_data dictionary"""
        if key not in self.cache_data or key is None:
            return None
        return self.cache_data.get(key)
