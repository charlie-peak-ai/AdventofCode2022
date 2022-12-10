"""https://adventofcode.com/2022/day/5"""
import re
from calendar import AdventOfCode
from typing import List, Tuple


class SupplyStacks(AdventOfCode):
    """Moves crates onto stacks using some instructions"""

    def __init__(self):
        super().__init__(strip_rows=False)

        self.task()
        self.task(multi_move=True)

    def task(self, multi_move: bool = False) -> None:
        """Finds what the top crate is per stack if one crate is moved at a time"""
        self._setup()
        move_list = self.get_moves_list()

        for i in move_list:
            self.apply_move(*i, multi_move=multi_move)

        top_stack_string = ""
        for stack_num, stack in self.stack_dict.items():
            print(f"{stack_num} - Top Crate: {stack[-1]}")
            top_stack_string += stack[-1][1]

        print(top_stack_string)

    def get_moves_list(self):
        """Iterates over rows with "move" in them and parses the individual instructions"""
        move_list = []
        for i in self.text_file:
            if "move" in i:
                quantity, origin_stack, dest_stack = self._parse_move_instructions(i)
                move_list.append([quantity, origin_stack, dest_stack])

        return move_list

    def apply_move(self, quantity: int, origin_stack: int, dest_stack: int, multi_move: bool = False) -> None:
        """Takes an instruction and moves n many crates"""
        print(f"Need to move {quantity} crates from {origin_stack} to {dest_stack}")
        if multi_move:
            self._move_crates(quantity, origin_stack, dest_stack)

        else:
            for i in range(quantity):
                self._move_crates(1, origin_stack, dest_stack)

    def _move_crates(self, move_quantity: int, origin_stack: int, dest_stack: int) -> None:
        crate_list = self._get_crates(origin_stack, move_quantity)
        print(f"Moving {crate_list} from {origin_stack} to {dest_stack}")
        self._remove_crate(origin_stack, move_quantity)
        self._add_crate(dest_stack, crate_list)

    def _get_crates(self, stack_num: int, num_crates: int) -> List[str]:
        """Gets the top most crate from a stack"""
        try:
            crate = self.stack_dict[stack_num][num_crates * -1 :]
            if isinstance(crate, str):
                crate = [crate]

            return crate

        except IndexError:
            print("Stack is empty")
            raise

    def _remove_crate(self, stack_num: int, quantity: int) -> None:
        """Removes n many crates from a stack"""
        del self.stack_dict[stack_num][quantity * -1 :]

    def _add_crate(self, stack_num: int, crate: list) -> None:
        """Extends a stack list by a list of crates"""
        self.stack_dict[stack_num].extend(crate)

    @staticmethod
    def _parse_move_instructions(move_row: str) -> Tuple[int, int, int]:
        """Extracts the number of crates to move and the stack numbers using regex"""
        pattern = r"move (\d+) from (\d+) to (\d+)"
        match = re.match(pattern, move_row)
        if match is not None:
            quantity, origin_stack, dest_stack = list(map(int, match.groups()))
            return quantity, origin_stack, dest_stack

    def _setup(self) -> None:
        parsed_crate_list = self._parse_starting_stack_positions()
        self.stack_dict = self._convert_to_stack_dict(parsed_crate_list)

    def _parse_starting_stack_positions(self) -> List[List[str]]:
        """Extracts the starting position of all crates on each stack"""
        parsed_crate_list = []
        for row in self.text_file:
            if "[" in row:
                new_row = self.chunker(row.replace("\n", ""), 4, distinct_groups=True)
                parsed_crate_list.append(list(new_row))

        return parsed_crate_list

    @staticmethod
    def _convert_to_stack_dict(parsed_crate_list: list) -> dict:
        """Converts the parsed lists of strings to dict of lists, reoriented as crate stacks"""
        stack_dict = {}
        for i, j in enumerate(zip(*parsed_crate_list), start=1):
            j = list(map(str.strip, j))
            j.reverse()
            j = [entry for entry in j if entry != ""]
            stack_dict[i] = j

        return stack_dict


if __name__ == "__main__":
    SupplyStacks()
