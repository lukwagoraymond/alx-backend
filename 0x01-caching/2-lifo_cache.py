#!/usr/bin/env python3
"""Module implements the LIFO caching replacement
policy"""

from collections import OrderedDict

BaseCaching = __import__('base_caching').BaseCaching


class LIFOCache(BaseCaching):
    """Implements the FIFO caching replacement
    policy"""

    def __init__(self):
        self.stack = list()
        super().__init__()

    def put(self, key, item):
        if key and item:
            self.cache_data.update({key: item})
            if key in self.stack:
                self.stack.remove(key)
            self.stack.append(key)
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            discarded_dict = self.stack.pop(-2)
            del self.cache_data[discarded_dict]
            print(f'DISCARD: {discarded_dict}')

    def get(self, key):
        """Returns a value of a particular key from
                self.cache_data dictionary"""
        if key not in self.cache_data or key is None:
            return None
        return self.cache_data.get(key)
