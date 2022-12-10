from calendar import AdventOfCode
from typing import List


class CampCleanup(AdventOfCode):
    def __init__(self):
        super().__init__()
        for i in self.text_file:
            print(i)

    def section_expander(self, input_data: List[str]):
        """Converts the input list from strings to lists of ints"""
        elf_pairs = 2


if __name__ == "__main__":
    CampCleanup()
