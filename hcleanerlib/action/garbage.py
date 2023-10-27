import os
import pathlib
import re

from hcleanerlib.utils.config import Configuration
from hcleanerlib.utils.explorer import Explorer
from hcleanerlib.utils.path import Path


class Garbage:
    """Remove empty folders, delete unwanted elements"""

    def __init__(self, config_type):
        self.__config = Configuration(config_type)
        self.__explorer = Explorer(config_type)
        self.__to_delete = self.__config.get_delete_pattern()

    def exec(self, source_folder_path: str, apply: bool = False, subdirectories: bool = False):

        source_folder = Path(source_folder_path)
        # TODO: refactor, as in the end, only on list can be returned
        elements_to_delete = []
        elements_deleted = []

        # Clean the base 1
        for element in self.__clean(source_folder_path):
            elements_to_delete.append(element)

        # Clean the different subdirectories found in the base 1
        if subdirectories:
            for folder in source_folder.folders():
                for element in self.__clean(folder):
                    elements_to_delete.append(element)

        if subdirectories:
            for subdirectory in source_folder.folders():
                sub = Path(subdirectory)
                # Delete if empty
                if sub.count() == 0:
                    elements_to_delete.append(subdirectory)
                else:
                    count = 0
                    for child in sub.children():
                        if child in elements_to_delete:
                            count = count + 1
                        else:
                            break
                    if count == sub.count():
                        elements_to_delete.append(subdirectory)

        if apply:
            for element in elements_to_delete:
                if os.path.isdir(element):
                    os.rmdir(element)
                else:
                    os.remove(element)
                if os.path.exists(element) is False:
                    elements_deleted.append(element)

        for element in elements_deleted:
            elements_to_delete.remove(element)

        return {
            "to_delete": elements_to_delete,
            "deleted": elements_deleted
        }

    def __clean(self, folder):
        """Yield element that should be deleted"""
        for element in Path(folder).files():
            if self.__is_to_delete(element):
                yield element

    def __is_to_delete(self, element):
        for pattern in self.__to_delete:
            if re.search(pattern, element) is not None:
                return True
        return False
