#!/usr/bin/env python3
"""Module Modifies the BaseCaching put and get
methods"""

BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):
    """Class inherits from BaseCaching and modifies
    its put and get methods"""

    def __init__(self):
        super().__init__()

    def put(self, key, item):
        """Assigns a value to a particular key"""
        if key is None and item is None:
            pass
        else:
            self.cache_data.update({key: item})

    def get(self, key):
        """Returns a value of a particular key from
        self.cache_data dictionary"""
        if key not in self.cache_data.keys() or key is None:
            return None
        return self.cache_data.get(key)

