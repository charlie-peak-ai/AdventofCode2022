"""https://adventofcode.com/2022/day/7"""
from __future__ import annotations

import re
from calendar import AdventOfCode
from pprint import pprint
from typing import List, Optional

from pydantic import BaseModel, Field


class DirObj(BaseModel):
    """Class to hold details for objects in a file system"""

    name: str = Field(..., description="Object name")
    type: str = Field(..., description="Object type, either dir or file")
    size: int = Field(0, description="The total size of this file. 0 if it is a directory")
    parent_dir: Optional[DirObj] = Field(None, description="The parent of this object")
    child_objects: Optional[List[DirObj]] = Field([], description="Child objects if this is a dir")

    dir_size: Optional[int] = Field(0, description="The total size in this directory. 0 if it is a file")

    class Config:
        validate_assignment = True


class NoSpaceLeftOnDevice(AdventOfCode):
    """Using some overkill Pydantic models, the directory structure can be modelled as a nested hierarchy"""

    def __init__(self):
        super().__init__()
        self.cwd = "/"
        self.cd_patten = r"\$ cd (.*)"

        self.root_object: DirObj = self._create_dir_obj("/", "dir")
        self.current_obj: DirObj = self.root_object

        self.dir_size_list = []
        self.max_dir_size = 100_000

        self.total_dir_size = 70_000_000
        self.update_size = 30_000_000

        self.task()

    def task(self):
        """Task to find file and directory sizes, using a set of instructions to model the structure."""

        row = self.text_file[0]
        if "$ ls" in row:
            print(f"Listing the contents of: {self._get_current_dir()}")

        elif "$ cd" in row:
            self._change_cwd(row)

        else:
            print(f"logging {row} as child of {self._get_current_dir()} --parent {self._get_current_parent()}")
            obj = self.parse_line(row)
            self.current_obj.child_objects.append(obj)

        self._get_size(self.root_object)
        self.find_all_small_dirs()
        self.find_smallest_size_to_fit_update()

    def find_smallest_size_to_fit_update(self) -> None:
        """Calculates what space is needed and what the smallest dir over that amount is"""
        current_space = self.total_dir_size - self.root_object.dir_size
        space_required = self.update_size - current_space

        sorted_list = sorted(self.dir_size_list, key=lambda i: i[1])
        pprint(sorted_list)
        print(f"Device has {current_space} and needs to clear {space_required}")

        dirs_over_x_size = [x for x in sorted_list if x[1] >= space_required]
        print(f"Deleting {dirs_over_x_size[0][0]} would save {dirs_over_x_size[0][1]}")

    def find_all_small_dirs(self) -> None:
        """Loops through list of directories, summing their size if it is below the threshold"""
        print(f"Locating all directories that are smaller than {self.max_dir_size}")
        small_dirs_total = 0
        for name, size in self.dir_size_list:
            if size <= self.max_dir_size:
                small_dirs_total += size

        print(small_dirs_total)

    def _get_size(self, dir_obj: DirObj) -> int:
        """Recursively sums the object sizes and assigns it the the total size attribute"""
        total_size = dir_obj.size
        for child_obj in dir_obj.child_objects:
            total_size += child_obj.size
            if child_obj.child_objects:
                total_size += self._get_size(child_obj)

        dir_obj.dir_size = total_size
        if dir_obj.type == "dir":
            self.dir_size_list.append((dir_obj.name, dir_obj.dir_size))

        return total_size

    @staticmethod
    def _create_dir_obj(
        name: str, _type: str, size: int = 0, parent_object: DirObj = None, child_objects: List[DirObj] = None
    ):
        """Creates the pydantic objects representing the file structure"""
        if child_objects is None:
            child_objects = []

        return DirObj(name=name, type=_type, size=size, parent_dir=parent_object, child_objects=child_objects)

    def parse_line(self, line: str) -> DirObj:
        """Takes a line and calls the appropriate method depending on contents"""
        if "dir" in line:
            obj = self._parse_dir(line)

        else:
            obj = self._parse_file(line)

        return obj

    def _parse_dir(self, line: str) -> DirObj:
        """Parses a directory object"""
        _, name = line.split(" ")
        obj = self._create_dir_obj(name, "dir", parent_object=self.current_obj)
        return obj

    def _parse_file(self, line: str) -> DirObj:
        """Parses a file object"""
        size, name = line.split(" ")
        obj = self._create_dir_obj(name, "file", size=size, parent_object=self.current_obj)
        return obj

    def _change_cwd(self, line: str) -> None:
        """Processes the cd command"""
        new_dir = re.match(self.cd_patten, line).groups()[0]
        new_dir = new_dir.strip()
        if new_dir == "/":
            print("Sitting at root")
            self.current_obj = self.current_obj

        elif new_dir == "..":
            print(f"Moving up from {self.current_obj.name} to {self.current_obj.parent_dir.name}")
            self.current_obj = self.current_obj.parent_dir

        else:
            print(f"Moving from {self.current_obj.name} to {new_dir}")
            try:
                self.current_obj = [i for i in self.current_obj.child_objects if i.name == new_dir][0]
            except IndexError:
                print([i.name for i in self.current_obj.child_objects])
                raise

        try:
            current_contents = self._extract_object_names(self.current_obj.child_objects)
            self.cwd = self._get_current_dir()
            print(f"Current {self.cwd} contents: {current_contents}")

        except Exception as e:
            print(e)
            raise

    @staticmethod
    def _extract_object_names(dir_objs: List[DirObj]) -> List[str]:
        current_contents = [i.name for i in dir_objs]
        return current_contents

    def _get_current_dir(self) -> str:
        return self.current_obj.name

    def _get_current_parent(self) -> str:
        try:
            return self.current_obj.parent_dir.name
        except AttributeError:
            return "No parent found"


if __name__ == "__main__":
    NoSpaceLeftOnDevice()
