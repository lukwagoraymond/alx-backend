#!/usr/bin/env python3
"""Module implements the LIFO caching replacement
policy"""


BaseCaching = __import__('base_caching').BaseCaching


class LIFOCache(BaseCaching):
    """Implements the FIFO caching replacement
    policy"""

    def __init__(self):
        self.stack = list()
        super().__init__()

    def put(self, key, item):
        """Adds item to cache memory"""
        if key and item:
            if len(self.cache_data) == self.MAX_ITEMS \
                    and key not in self.stack:
                discarded_dict = self.stack.pop()
                del self.cache_data[discarded_dict]
                print("DISCARD: {}".format(discarded_dict))
            self.cache_data.update({key: item})
            self.stack.append(key)

    def get(self, key):
        """Returns a value of a particular key from
                self.cache_data dictionary"""
        return self.cache_data.get(key)
