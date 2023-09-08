import json
import logging
import os
import pathlib
import shutil
from datetime import datetime

from hcleanerlib.utils.explorer import Explorer
from hcleanerlib.utils.path import Path


class Integrity:
    def __init__(self, config_type):
        self.__explorer = Explorer(config_type)

    def exec(self, folder, delete_corrupted, subdirectories):
        """Check image file integrity"""
        parent = Path(folder)

        if subdirectories:
            for sub_folder in parent.folders():
                yield f"Checking {sub_folder} folder"
                current = Path(sub_folder)
                corrupted = self.__get_corrupted_count(current)
                if corrupted > 0:
                    yield f"{current.name()} contains {corrupted} corrupted images ({corrupted / current.count() * 100}%)"
                    if delete_corrupted and corrupted == current.count():
                        yield f"{sub_folder} deleted"
                        shutil.rmtree(current.fullpath())
                else:
                    yield "No corrupted files found"
        else:
            yield f"Checking {folder} folder"

            corrupted = self.__get_corrupted_count(parent)
            if corrupted > 0:
                yield f"{folder} contains {corrupted} corrupted images ({corrupted / parent.count() * 100}%)"
                if delete_corrupted and corrupted == parent.count():
                    yield f"{folder} deleted"
                    shutil.rmtree(parent.fullpath())
            else:
                yield "No corrupted files found"
        return

    def __get_corrupted_count(self, folder):
        corrupted = 0
        for file in folder.files():
            if self.__explorer.is_image(file) and self.__explorer.is_image_corrupted(file):
                corrupted = corrupted + 1

        return corrupted
