#!/usr/bin/env python3
"""Module implements the LIFO caching replacement
policy"""

from collections import OrderedDict

BaseCaching = __import__('base_caching').BaseCaching


class LIFOCache(BaseCaching):
    """Implements the FIFO caching replacement
    policy"""

    def __init__(self):
        self.ordered_cache_data = OrderedDict()
        super().__init__()

    def put(self, key, item):
        if key and item:
            if len(self.ordered_cache_data) == BaseCaching.MAX_ITEMS:
                if key not in self.ordered_cache_data:
                    discarded_dict = self.ordered_cache_data.popitem(last=True)
                    print(f'DISCARD: {discarded_dict[0]}')
                    self.ordered_cache_data.update({key: item})
                elif key in self.ordered_cache_data:
                    print(f'DISCARD: {key}')
                    self.ordered_cache_data.update({key: item})
                stored_keys = [keys for keys in self.ordered_cache_data.keys()]
                self.cache_data.clear()
                for keys in stored_keys:
                    self.cache_data.update(
                        {keys: self.ordered_cache_data[keys]})

            elif len(self.cache_data) < 5:
                self.cache_data.update({key: item})
                self.ordered_cache_data.update({key: item})

    def get(self, key):
        """Returns a value of a particular key from
                self.cache_data dictionary"""
        if key not in self.cache_data or key is None:
            return None
        return self.cache_data.get(key)
