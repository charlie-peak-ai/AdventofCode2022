"""https://adventofcode.com/2022/day/6"""
from calendar import AdventOfCode
from typing import List


class TuningTrouble(AdventOfCode):
    """Crawling through a long string to detect a unique set of characters"""

    def __init__(self):
        super().__init__()

        self.packet_num_chars = 4
        self.message_num_chars = 14

        self.task()

    def task(self):
        """Locating specific strings of lengths 4 and 14"""
        row: str
        for row in self.text_file:
            market_pos = self.locate_markers(row, self.packet_num_chars)
            print(f"There are {market_pos} chars before first market detected")

            market_pos = self.locate_markers(row, self.message_num_chars)
            print(f"There are {market_pos} chars before first message detected")

    def locate_markers(self, data_stream: str, num_unique_chars_to_find: int) -> int:
        """Iterates through the stream and locates unique chars of a given length"""

        marker_list = []
        for s in self._split_data_stream_to_chunks(data_stream, num_unique_chars_to_find):
            if len(set(s)) == num_unique_chars_to_find:
                marker_list.append(s)

        first_marker_pos = data_stream.find("".join(marker_list[0]))
        return first_marker_pos + num_unique_chars_to_find

    def _split_data_stream_to_chunks(self, data_stream: str, num_chars_to_group_to: int) -> List[str]:
        """Converts the long data string to a list of strings, crawled forward one character at a time"""

        split_strings = list(self.chunker(data_stream, num_chars_to_group_to, distinct_groups=False))
        return split_strings


if __name__ == "__main__":
    TuningTrouble()
