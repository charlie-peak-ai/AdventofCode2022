"""https://adventofcode.com/2022/day/3"""
import logging
import string
from typing import List, TextIO


class RucksackSorter:
    """Finds common elements in strings"""

    def __init__(self):
        self.text_file = "input.txt"
        self.priority_dict = self._priority()

        self.task_one()
        self.task_two()

    def task_one(self) -> None:
        """Compares the two rucksack compartments for common elements and values them"""
        raw_data = self._open_file()
        rucksack_list = self._strip_data(raw_data)
        value_list = []
        for rucksack in rucksack_list:
            rucksack_half_point = len(rucksack) // 2
            compartment_1, compartment_2 = rucksack[:rucksack_half_point], rucksack[rucksack_half_point:]
            common_elements = self.find_intersection([compartment_1, compartment_2])
            value_list.extend(self.find_and_value_occurrences(common_elements))

        self._calc_value(value_list)

    def task_two(self) -> None:
        """Identify the item that is in all bags per 3 elf groupings"""
        print("=" * 20)
        raw_data = self._open_file()
        rucksack_list = self._strip_data(raw_data)

        value_list = []
        grouped_rucksacks = self.group_elves(rucksack_list)
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

    def _open_file(self) -> TextIO:
        """Opens the file into memory"""
        logging.debug(f"Opening file: {self.text_file}")
        raw_data = open(self.text_file)

        return raw_data

    @staticmethod
    def _strip_data(raw_data: TextIO) -> List[str]:
        """Iterates over the raw TextIO object and writes stripped lines to a list"""
        stripped_data = []
        for row in raw_data:
            stripped_data.append(row.strip())
        return stripped_data


if __name__ == "__main__":
    RucksackSorter()
