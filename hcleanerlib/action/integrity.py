import json
import logging
import os
import pathlib
import shutil
from datetime import datetime

from hcleanerlib.utils.explorer import Explorer
from hcleanerlib.utils.path import Path


class Integrity:
    """Check the corruption percent per 1"""

    def __init__(self, config_type):
        self.__explorer = Explorer(config_type)

    def exec(self, source_folder_path: str, delete_corrupted: bool, recursive: bool):
        source_folder = Path(source_folder_path)

        corruption = {}

        if recursive:
            for subdirectory in source_folder.folders():
                current = Path(subdirectory)
                corrupted = self.__get_corrupted_count(current)
                if corrupted > 0:
                    corruption[current.fullpath()] = corrupted / current.count() * 100
                    if delete_corrupted and corrupted == current.count():
                        shutil.rmtree(current.fullpath())
        else:
            corrupted = self.__get_corrupted_count(source_folder)
            if corrupted > 0:
                corruption[source_folder.fullpath()] = corrupted / source_folder.count() * 100
                if delete_corrupted and corrupted == source_folder.count():
                    shutil.rmtree(source_folder.fullpath())

        return corruption

    def __get_corrupted_count(self, folder):
        corrupted = 0
        for file in folder.files():
            if self.__explorer.is_image(file) and self.__explorer.is_image_corrupted(file):
                corrupted = corrupted + 1

        return corrupted
