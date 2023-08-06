import io
import struct
from operator import itemgetter
from typing import Iterable, Any
from functools import lru_cache
from siphashc import siphash


MAX_INDEX = 4294967295  # 2^32 - 1
STRUCT_DEF = "I I I"  # 4 byte unsigned int, 4 byte unsigned int, 4 byte unsigned int
RECORD_SIZE = struct.calcsize(STRUCT_DEF)  # this should be 12

"""
There are overlapping terms because we're traversing a dataset so we can traverse a
dataset. 

Terminology:
    Entry     : a record in the Index
    Position  : the position of the entry in the Index
    Location  : the position of the row in the target file
    Row       : a record in the target file
"""


class Index:

    def __init__(self, index: io.BytesIO):
        """
        A data index which speeds up reading data files.

        The file format is fixed-length binary, the search algorithm is a
        classic binary search.
        """
        print("LOADING AN INDEX")
        if isinstance(index, io.BytesIO):
            # go to the end of the stream
            index.seek(0, 2)
            # divide the size of the stream by the record size to get the
            # number of entries in the index
            self.size = index.tell() // RECORD_SIZE

            # create a view of the index for look ups
            index.seek(0, 0)
            self._index = memoryview(index.read())

    @staticmethod
    def build_index(dictset: Iterable[dict], column_name: str):
        """
        Build an index from a dictset.

        Parameters:
            dictset: iterable of dictionaries
                The dictset to index
            column_name: string
                The name of the index which will be indexed

        Returns:
            io.BytesIO
        """
        # We do this in two-steps
        # 1) Build an intermediate form of the index as a list of entries
        # 2) Conver that intermediate form into a binary index
        builder = IndexBuilder(column_name)
        for position, row in enumerate(dictset):
            builder.add(position, row)
        return builder.build()

    def _get_entry(self, position: int):
        """
        get a specific entry from the index
        """
        try:
            start = RECORD_SIZE * position
            value, loc, count = struct.unpack_from(
                STRUCT_DEF, self._index[start : start + RECORD_SIZE]
            )
            return (value, loc, count)
        except Exception:
            return None, None, None

    def _locate_record(self, value):
        """
        Use a binary search algorithm to search the index
        """
        left, right = 0, (self.size - 1)
        while left <= right:
            middle = (left + right) >> 1
            v, l, c = self._get_entry(middle)
            if v == value:
                return middle, v, l, c
            elif v > value:
                right = middle - 1
            else:
                left = middle + 1
        return -1, None, None, None

    def _inner_search(self, search_term) -> Iterable:
        # hash the value and make fit in a four byte unsinged int
        value = siphash("*" * 16, f"{search_term}") % MAX_INDEX

        # search for an instance of the value in the index
        location, v, l, c = self._locate_record(value)

        # we didn't find the entry
        if location < 0:
            return []

        # the found_entry is the fastest record to be found, this could
        # be the first, last or middle of the set. The count field tells
        # us how many rows to go back, but not how many forward
        start_location = location - c + 1
        end_location = location + 1
        while end_location < self.size and self._get_entry(end_location)[0] == value:
            end_location += 1

        # extract the row numbers in the target dataset
        return [
            self._get_entry(loc)[1] for loc in range(start_location, end_location, 1)
        ]

    def search(self, search_term) -> Iterable:
        """
        Search the index for a value. Returns a list of row numbers, if the value is
        not found, the list is empty.
        """
        if not isinstance(search_term, (list, set, tuple)):
            search_term = [search_term]
        result: list = []
        for term in search_term:
            result[0:0] = self._inner_search(term)
        return set(result)

    def dump(self, file):
        with open(file, "wb") as f:
            f.write(self._index[:])

    def bytes(self):
        return self._index[:]


class IndexBuilder:

    slots = ("column_name", "temporary_index")

    def __init__(self, column_name: str):
        self.column_name: str = column_name
        self.temporary_index: Iterable[dict] = []

    def add(self, position, record):
        ret_val = []
        if record.get(self.column_name):
            # index lists of items separately
            values = record[self.column_name]
            if not isinstance(values, list):
                values = [values]
            for value in values:
                entry = {
                    "val": siphash("*" * 16, f"{value}") % MAX_INDEX,
                    "pos": position,
                }
                ret_val.append(entry)
        self.temporary_index += ret_val
        return ret_val

    def build(self) -> Index:
        previous_value = None
        index = bytes()
        count: int = 0
        self.temporary_index = sorted(self.temporary_index, key=itemgetter("val"))
        for row in self.temporary_index:
            if row["val"] == previous_value:
                count += 1
            else:
                count = 1
            index += struct.pack(STRUCT_DEF, row["val"], row["pos"], count)
            previous_value = row["val"]
        return Index(io.BytesIO(index))
