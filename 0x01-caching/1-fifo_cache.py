#!/usr/bin/env python3
"""Module implements the FIFO caching replacement
policy"""

from collections import deque

BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache(BaseCaching):
    """Implements the FIFO caching replacement
    policy"""

    def __init__(self):
        self.queue = []
        self.ordered_cache_data = deque([])
        super().__init__()

    """def put(self, key, item):
        \"""Assigns value to cache\"""
        if key and item:
            self.cache_data[key] = item
            if key not in self.queue:
                self.queue.append(key)

        if len(self.queue) > self.MAX_ITEMS:
            popped = self.queue.pop(0)
            del self.cache_data[popped]
            print(f"DISCARD: {popped}")"""

    def put(self, key, item):
        if key and item:
            if len(self.cache_data) == BaseCaching.MAX_ITEMS \
                    and key not in self.ordered_cache_data:
                discarded_dict = self.ordered_cache_data.popleft()
                del self.cache_data[discarded_dict]
                print(f'DISCARD: {discarded_dict}')
            self.cache_data.update({key: item})
            self.ordered_cache_data.append(key)

    def get(self, key):
        """Returns a value of a particular key from
                self.cache_data dictionary"""
        if key not in self.cache_data or key is None:
            return None
        return self.cache_data.get(key)
