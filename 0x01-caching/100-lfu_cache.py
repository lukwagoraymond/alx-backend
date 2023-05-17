#!/usr/bin/python3
"""Module implements the LFU caching replacement
policy"""

from datetime import datetime
from collections import defaultdict
BaseCaching = __import__('base_caching').BaseCaching


class LFUCache(BaseCaching):
    """Implements the LFU caching replacement
    policy"""

    def __init__(self):
        """Instantiation"""
        self.cache_by_time = {}
        self.cache_by_frequency_use = defaultdict(int)  # >>> Default value: 0
        super().__init__()

    def put(self, key, item):
        if key and item:
            self.cache_by_time[key] = datetime.now()
            self.cache_data[key] = item
            self.cache_by_frequency_use[key] += 1

            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                # Sorted elements by frequency_used
                frequency_use_filtered = {}
                for k, v in self.cache_by_frequency_use.items():
                    if k != key:
                        frequency_use_filtered[k] = v
                keys_by_frequency_used = sorted(frequency_use_filtered,
                                                key=frequency_use_filtered.get)
                key_to_delete = keys_by_frequency_used[0]

                # There are more elements with same frequency used count?
                count = frequency_use_filtered[key_to_delete]
                posibles_elements_to_discard_dict = {}
                for k, v in frequency_use_filtered.items():
                    if v == count:
                        posibles_elements_to_discard_dict[k] = v
                if len(posibles_elements_to_discard_dict) > 1:
                    elements_to_discard_by_time = {}
                    for k, v in self.cache_by_time.items():
                        if k in posibles_elements_to_discard_dict.keys():
                            elements_to_discard_by_time[k] = v

                    elements_by_time = sorted(
                        elements_to_discard_by_time,
                        key=elements_to_discard_by_time.get)
                    key_to_delete = elements_by_time[0]

                # Delete element with least_frequency_used
                del self.cache_by_time[key_to_delete]
                del self.cache_data[key_to_delete]
                del self.cache_by_frequency_use[key_to_delete]
                print('DISCARD: {}'.format(key_to_delete))

    def get(self, key):
        """Returns a value of a particular key from
                self.cache_data dictionary"""
        element = self.cache_data.get(key)
        if element:
            self.cache_by_time[key] = datetime.now()
            self.cache_by_frequency_use[key] += 1
        return element
