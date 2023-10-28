import os
import pathlib
import re
import shutil
from typing import List


class Path:
    """Represent a file system element and allow to perform action on it."""

    def __init__(self, path: str):
        if os.path.exists(path) is False:
            raise FileNotFoundError(f"No element found for path {path}")

        if not self.__is_absolute(path):
            self.__fullpath = self.__simplify(os.path.join(os.getcwd(), path))
        else:
            self.__fullpath = self.__simplify(path)

        self.__is_folder = os.path.isdir(self.__fullpath)

    @staticmethod
    def __is_absolute(path: str):
        return (
            path.startswith("/") or re.match("^[a-zA-Z]:[/\\\\]", path) or path.startswith("\\\\")
        )

    @staticmethod
    def __simplify(path: str):
        parts = path.split("\\")
        result_array: List = []
        for part in parts:
            if part == "..":
                result_array = result_array[:-1]
            elif part == ".":
                continue
            else:
                result_array.append(part)

        return "\\".join(result_array)

    def fullpath(self):
        """Return the absolute path of an element, itself included at the end."""
        return self.__fullpath

    def is_folder(self):
        """Check if the element is a folder."""
        return self.__is_folder

    def count(self):
        """Return the number of elements inside the path if it's a folder itself."""
        if not self.is_folder():
            return None
        return len(self.files()) + len(self.folders())

    def children(self, no_parent=False):
        """Return a list which represent the element content if it's a folder itself."""
        if not self.is_folder():
            return None

        if no_parent:
            return os.listdir(self.fullpath())

        result = []
        for element in os.listdir(self.fullpath()):
            result.append(os.path.join(self.fullpath(), element))
        return result

    def files(self, no_parent=False):
        """Return the list of the element's files if it's a folder itself."""
        if not self.is_folder():
            return None
        files = []
        for element in self.children(no_parent):
            file = os.path.join(self.__fullpath, element)
            if os.path.isfile(file):
                files.append(element)
        return files

    def folders(self, no_parent=False):
        """Return the list of the element's folders if it's a folder itself."""
        if not self.is_folder():
            return None
        folders = []
        for element in self.children(no_parent):
            folder = os.path.join(self.__fullpath, element)
            if os.path.isdir(folder):
                folders.append(element)
        return folders

    def move(self, destination: str, force=False):
        """
        Move the element to a new location.
        If an element with the same name exists at the new location
        the method raise an exception except if the force
        parameter is set to true
        """
        current = self.fullpath()

        if not self.__is_absolute(destination):
            destination = os.path.join(self.path(), destination)

        destination = self.__simplify(destination)

        new_location = os.path.join(destination, self.name())

        if os.path.exists(new_location) and force is False:
            raise FileExistsError("An element with the same name already exist at this location")

        os.makedirs(destination, exist_ok=True)
        self.__fullpath = new_location
        if self.__is_parent(current, self.__fullpath):
            for element in os.listdir(current):
                shutil.move(os.path.join(current, element), self.__fullpath)
            os.rmdir(current)
        else:
            shutil.move(current, self.fullpath())

    @staticmethod
    def __is_parent(current_path: str, new_path: str):
        cp = current_path.split(os.sep)
        np = new_path.split(os.sep)

        return len(cp) == len(np) + 1 and current_path.startswith(new_path)

    def name(self):
        """Return the element name."""
        return pathlib.Path(self.fullpath()).name

    def path(self):
        """Return the location of the element."""
        return os.path.dirname(self.fullpath())
