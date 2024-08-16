#!/usr/bin/env python3
"""1_simple_pagination"""
import csv
import math
from typing import List, Tuple


class Server:
    """server"""
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """the datase"""
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """method named get_page"""
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0
        total_pages = math.ceil(len(self.dataset()) / page_size)
        if page < 1 or page > total_pages:
            return []
        start, end = self.index_range(page, page_size)
        return self.dataset()[start:end]

    def index_range(self, page: int, page_size: int) -> Tuple[int, int]:
        """ find the correct indexes to paginate the dataset
        correctly and return the appropriate page of the dataset"""
        total_rows = len(self.dataset())
        total_pages = math.ceil(total_rows / page_size)
        start = (page - 1) * page_size
        end = min(start + page_size, total_rows)
        return start, end
