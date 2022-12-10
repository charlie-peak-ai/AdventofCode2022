"""https://adventofcode.com/2022/day/4"""
from calendar import AdventOfCode
from typing import List, Tuple


class CampCleanup(AdventOfCode):
    """Finds overlaps between lists of ints"""

    def __init__(self):
        super().__init__()

        self.task_one()
        self.task_two()

    def task_one(self):
        """Finding full overlaps between sections"""
        expanded_elf_pairs = self.section_expander(self.text_file)
        self.find_full_overlaps(expanded_elf_pairs)

    def task_two(self):
        """Finding partial overlaps between sections"""
        expanded_elf_pairs = self.section_expander(self.text_file)
        self.find_partial_overlaps(expanded_elf_pairs)

    def section_expander(self, input_data: List[str]) -> list[list[list[int]]]:
        """Converts the input list from strings to lists of ints"""
        expanded_list = []
        for row in input_data:
            elf_pairs = row.split(",")
            elf_pair_list = []
            for elf in elf_pairs:
                areas = elf.split("-")
                min_area, max_area = self._find_min_max(areas)
                filled_in_area_list = self._fill_in_ints(min_area, max_area)

                elf_pair_list.append(filled_in_area_list)
            expanded_list.append(elf_pair_list)

        return expanded_list

    @staticmethod
    def find_full_overlaps(expanded_list: list):
        """Checks if a section pairing FULLY contains the other"""
        overlap_count = 0
        for elf_pairing in expanded_list:
            elf_set_1 = set(elf_pairing[0])
            elf_set_2 = set(elf_pairing[1])

            if elf_set_1.issubset(elf_set_2):
                print(f"Elf1 is subset of Elf2", min(elf_set_1), max(elf_set_1), "--", min(elf_set_2), max(elf_set_2))
                overlap_count += 1

            elif elf_set_1.issuperset(elf_set_2):
                print(f"Elf1 is superset of Elf2", min(elf_set_1), max(elf_set_1), "--", min(elf_set_2), max(elf_set_2))
                overlap_count += 1

            else:
                pass

        print(f"There were {overlap_count} total full overlaps")

    @staticmethod
    def find_partial_overlaps(expanded_list: list) -> None:
        """Checks if there are ANY overlaps in the sections"""
        overlap_count = 0
        for elf_pairing in expanded_list:
            elf_pairing_set_list = list(map(set, elf_pairing))
            overlap_set = set.intersection(*elf_pairing_set_list)
            if overlap_set:
                print(f"Overlaps found: {min(overlap_set)} - {max(overlap_set)}")
                overlap_count += 1

        print(f"There were {overlap_count} total partial overlaps")

    @staticmethod
    def _find_min_max(areas: List[str]) -> Tuple[int, int]:
        areas = list(map(int, areas))

        min_area = min(areas)
        max_area = max(areas)
        return min_area, max_area

    @staticmethod
    def _fill_in_ints(min_val: int, max_val: int) -> List[int]:
        """Using 2 int values, forms a list with all values between and including them"""
        lst = [i for i in range(min_val, max_val + 1)]
        return lst


if __name__ == "__main__":
    CampCleanup()
