#!/usr/bin/env python3
"""
Deletion-resilient hypermedia_pagination
"""
import csv
import math
from typing import List, Dict


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = {}  # Initialize as an empty dictionary

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """Implement a get_hyper_index method """
        items = len(self.dataset())
        total_pages = math.ceil(items / page_size)

        # Check if the given index is None or out of range
        if index is None or index < 0 or index >= total_pages:
            return {
                "page_size": page_size,
                "page": 0,
                "total_pages": total_pages,
                "page_size": 0,
                "items": items,
                "start_index": 0
            }

        # Calculate the starting index for the requested page
        start_index = index * page_size

        # Calculate the actual page based on the start index
        page = start_index // page_size + 1

        # Calculate next_index based on its existence
        next_index = (index + 1) if (index + 1) < total_pages else None

        # Delete the entry from the indexed dataset if it exists
        if index is not None and index in self.__indexed_dataset:
            del self.__indexed_dataset[index]

        return {
            "page_size": page_size,
            "page": page,
            "total_pages": total_pages,
            "items": items,
            "start_index": start_index,
            "next_index": next_index
        }

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        items = len(self.dataset())
        indexed_data = {}
        for i in range(items):
            indexed_data[i] = self.dataset()[i]
        return indexed_data
