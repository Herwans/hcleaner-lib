import logging
import os
import pathlib
import re
import shutil


class Path:
    def __init__(self, path: str):
        if os.path.exists(path) is False:
            raise FileNotFoundError(f"No element found for path {path}")

        if not self.__is_absolute(path):
            self.__fullpath = self.__simplify(os.path.join(os.getcwd(), path))
        else:
            self.__fullpath = self.__simplify(path)

        self.__is_dir = os.path.isdir(self.__fullpath)

    @staticmethod
    def __is_absolute(path: str):
        return path.startswith('/') or re.match("^[a-zA-Z]:[/\\\\]", path) or path.startswith('\\\\')

    @staticmethod
    def __simplify(path: str):
        parts = path.split('\\')
        result_array = []
        for part in parts:
            if part == "..":
                result_array = result_array[:-1]
            elif part == ".":
                continue
            else:
                result_array.append(part)

        return "\\".join(result_array)

    def fullpath(self):
        return self.__fullpath

    def is_dir(self):
        return self.__is_dir

    def count(self):
        if not self.is_dir():
            return None
        return len(self.files()) + len(self.folders())

    def children(self, no_parent=False):
        if not self.is_dir():
            return None

        if no_parent:
            return os.listdir(self.fullpath())
        else:
            result = []
            for element in os.listdir(self.fullpath()):
                result.append(os.path.join(self.fullpath(), element))
            return result

    def files(self, no_parent=False):
        if not self.is_dir():
            return None
        files = []
        for element in self.children():
            file = os.path.join(self.__fullpath, element)
            if os.path.isfile(file):
                if no_parent:
                    files.append(element)
                else:
                    files.append(file)
        return files

    def folders(self, no_parent=False):
        if not self.is_dir():
            return None
        folders = []
        for element in self.children():
            folder = os.path.join(self.__fullpath, element)
            if os.path.isdir(folder):
                if no_parent:
                    folders.append(element)
                else:
                    folders.append(folder)
        return folders

    def move(self, destination: str):
        current = self.fullpath()

        if not self.__is_absolute(destination):
            destination = os.path.join(self.path(), destination)

        destination = self.__simplify(destination)

        new_location = os.path.join(destination, self.name())

        if os.path.exists(new_location):
            raise FileExistsError("An element with the same name already exist at this location")
        else:
            os.makedirs(destination, exist_ok=True)
            self.__fullpath = new_location
            shutil.move(current, self.fullpath())

    def name(self):
        return pathlib.Path(self.fullpath()).name

    def path(self):
        return os.path.dirname(self.fullpath())