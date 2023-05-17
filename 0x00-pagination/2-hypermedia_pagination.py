#!/usr/bin/env python3
"""Simple Helper Function named index_range"""
import csv
import math
from typing import List
from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple:
    """Function returns a tuple of size two
    containing a start index and an end index"""
    return (page - 1) * page_size, page * page_size


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
  Function that takes two integer arguments.

  Args:
    page: current page being searched
    page_size: Number of rows on each page

  Returns:
    Correct list of rows of the dataset being searched
  """
        assert type(page) is int and page > 0
        assert type(page_size) is int and page_size > 0
        # Get Data from csv file
        dataset = self.dataset()
        try:
            tup_index = index_range(page, page_size)
            range_index = list(tup_index)
            return dataset[range_index[0]:range_index[1]]
        except IndexError:
            return list()

    def get_hyper(self, page: int = 1, page_size: int = 10) -> dict:
        """
          Function that takes two integer arguments.

          Args:
            page: current page being searched
            page_size: Number of rows on each page

          Returns:
            Dictionary containing the page_size, page, data, next_page,
            prev_page, total_pages
          """
        data = self.get_page(page, page_size)
        total_pages = math.ceil(len(self.dataset()) / page_size)
        next_page = page + 1 if page < total_pages else None
        prev_page = page - 1 if page > 1 else None

        return {
            "page_size": len(data),
            "page": page,
            "data": data,
            "next_page": next_page,
            "prev_page": prev_page,
            "total_pages": total_pages
        }
