"""https://adventofcode.com/2022/day/1"""
from calendar import AdventOfCode
from typing import List


class ElfCalories(AdventOfCode):
    """Calorie Finder"""

    def __init__(self):
        super().__init__()
        self.elf_list = None

        self.main()

    def main(self) -> None:
        """Main function"""

        self.elf_list = self.sum_calories(self.text_file)

        print("==== Task 1 ====")
        self.find_top_n_elves(1)

        print("==== Task 2 ====")
        self.find_top_n_elves()

    @staticmethod
    def sum_calories(data: List[str]) -> list:
        """
        Iterates over the opened file, stripping the read-in lines of any line breaks and summing the values.

        If the row is empty that means this is the delimiter between elves.
        The calorie values need to be written to the list, and the sum reset.
        """
        elf_list = []
        current_cals = 0
        for row in data:

            if row == "":
                elf_list.append(current_cals)
                current_cals = 0

            else:
                current_cals += int(row)

        return elf_list

    def find_top_n_elves(self, num_elves: int = 3) -> None:
        """Part 2, Finding the elves that brought the top 3 amount of calories."""
        _elf_list = self.elf_list.copy()
        _elf_list.sort()

        total_kcal = 0
        for i in range(num_elves):
            print(f"Finding the elf who brought the #{i + 1} most calories")
            index_val = i + 1
            kcal = _elf_list[-index_val]
            total_kcal += kcal
            self._elf_finder(kcal)

        print(f"\nThe top {num_elves} brought {total_kcal}\n")

    def _elf_finder(self, kcal: int):
        """Takes an input kcal amount and finds the elf that holds that much"""
        elf_number = self.elf_list.index(kcal)
        print(f"Elf: {elf_number + 1} brought {self.elf_list[elf_number]} calories")


if __name__ == "__main__":
    ElfCalories()
