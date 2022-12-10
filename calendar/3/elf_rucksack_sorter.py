"""https://adventofcode.com/2022/day/3"""
import string
from calendar import AdventOfCode
from typing import List


class RucksackSorter(AdventOfCode):
    """Finds common elements in strings"""

    def __init__(self):
        super().__init__()
        self.priority_dict = self._priority()

        self.task_one()
        self.task_two()

    def task_one(self) -> None:
        """Compares the two rucksack compartments for common elements and values them"""
        value_list = []
        for rucksack in self.text_file:
            rucksack_half_point = len(rucksack) // 2
            compartment_1, compartment_2 = rucksack[:rucksack_half_point], rucksack[rucksack_half_point:]
            common_elements = self.find_intersection([compartment_1, compartment_2])
            value_list.extend(self.find_and_value_occurrences(common_elements))

        self._calc_value(value_list)

    def task_two(self) -> None:
        """Identify the item that is in all bags per 3 elf groupings"""
        print("=" * 20)

        value_list = []
        grouped_rucksacks = self.group_elves(self.text_file)
        for group in grouped_rucksacks:
            common_elements = self.find_intersection(group)
            value_list.extend(self.find_and_value_occurrences(common_elements))

        self._calc_value(value_list)

    @staticmethod
    def group_elves(raw_data: List[str], group_size: int = 3) -> List[List[str]]:
        """Groups up the rows to sets of 3"""
        elf_list = []
        sub_list = []
        for e, rucksack in enumerate(raw_data, start=1):
            sub_list.append(rucksack)
            if e % group_size == 0:
                elf_list.append(sub_list)
                sub_list = []

        if sub_list:
            elf_list.append(sub_list)

        return elf_list

    @staticmethod
    def find_intersection(list_of_rucksacks: List[str]) -> set:
        """Finds common element in list of given rucksacks"""
        set_list = [set(i) for i in list_of_rucksacks]
        intersection = set.intersection(*set_list)
        return intersection

    def find_and_value_occurrences(self, common_elements: set) -> List[int]:
        """
        Uses the known common items and the priority_dict to determine a score value.

        Returns a list in case of multiple common elements
        """

        return [self.priority_dict.get(i) for i in common_elements]

    @staticmethod
    def _calc_value(value_list: List[int]) -> None:
        """Sums up the values in the list of dicts"""
        print(sum(value_list))

    @staticmethod
    def _priority() -> dict:
        all_chars = string.ascii_lowercase + string.ascii_uppercase
        priority_dict = {}
        for e, i in enumerate(all_chars, start=1):
            priority_dict[i] = e

        return priority_dict


if __name__ == "__main__":
    RucksackSorter()
