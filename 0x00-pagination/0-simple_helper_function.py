#!/usr/bin/env python3
"""Simple Helper Function named index_range"""

from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple:
    """Function returns a tuple of size two
    containing a start index and an end index"""
    return (page - 1) * page_size, page * page_size
