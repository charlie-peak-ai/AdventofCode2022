import logging
from typing import Collection, Generator, List, TextIO


class AdventOfCode:
    """Base class that loads up the input data"""

    def __init__(self, strip_rows: bool = True):
        self.input_file_location = "./input.txt"
        raw_data = self._open_file()
        self.text_file: List[str] = self._data_to_list(raw_data, strip_rows)

    def _open_file(self) -> TextIO:
        """Opens the file into memory"""
        logging.debug(f"Opening file: {self.input_file_location}")
        raw_data = open(self.input_file_location)

        return raw_data

    @staticmethod
    def _data_to_list(raw_data: TextIO, strip: bool = True) -> List[str]:
        """Iterates over the raw TextIO object and writes stripped lines to a list"""
        stripped_data = []
        for row in raw_data:
            if strip:
                stripped_data.append(row.strip())
            else:
                stripped_data.append(row)
        return stripped_data

    @staticmethod
    def chunker(seq: Collection, size: int, distinct_groups: bool = True) -> Generator:
        """
        Takes any iterable and steps through it in chunks

        Notes
        ------
        If distinct groups is selected then it will step forward through the iterable.
        Eg "abcdefghi" with size 3 would become "abc", "def", "ghi" etc

        Otherwise, will step forward by 1 position each time.
        Eg "abcdefghi" with size 3 would become "abc", "bcd", "cde" etc
        """
        if distinct_groups:
            return (seq[pos : pos + size] for pos in range(0, len(seq), size))
        else:
            return (seq[pos : pos + size] for pos in range(0, len(seq)))
