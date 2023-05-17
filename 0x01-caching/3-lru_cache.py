#!/usr/bin/env python3
"""Module implements the LRU caching replacement
policy"""

from datetime import datetime
BaseCaching = __import__('base_caching').BaseCaching


class LRUCache(BaseCaching):
    """Implements the LRU caching replacement
    policy"""

    def __init__(self):
        self.stack = list()
        super().__init__()

    def put(self, key, item):
        """Add an item in the cache memory
        """
        if key and item:
            if len(self.cache_data) == BaseCaching.MAX_ITEMS\
                    and key not in self.stack:
                discard_key = self.stack.pop(0)
                del self.cache_data[discard_key]
                print("DISCARD: {}".format(discard_key))
            if key in self.stack:
                self.stack.remove(key)
            self.cache_data.update({key: item})
            self.stack.append(key)

    """def put(self, key, item):
        if key and item:
            if len(self.cache_data) == BaseCaching.MAX_ITEMS\
                    and key not in self.stack:
                discard_key = self.stack.pop(0)
                del self.cache_data[discard_key]
                print(f'DISCARD: {discard_key}')
            if key in self.stack:
                self.stack.remove(key)
            self.cache_data.update({key: item})
            self.stack.append(key)"""

    def get(self, key):
        """Returns a value of a particular key from
                self.cache_data dictionary"""
        if key in self.stack:
            self.stack.remove(key)
            self.stack.append(key)
        return self.cache_data.get(key)
