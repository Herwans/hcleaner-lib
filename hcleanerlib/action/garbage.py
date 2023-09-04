import logging
import os
import pathlib
import re

from hcleanerlib.utils.config import Configuration
from hcleanerlib.utils.explorer import Explorer
from hcleanerlib.utils.path import Path


class Garbage:
    def __init__(self, config_type):
        self.__config = Configuration(config_type)
        self.__explorer = Explorer(config_type)
        self.__to_delete = self.__config.get_delete_pattern()

    def exec(self, folder, apply, sub):
        """Remove empty folders, delete unwanted elements"""
        self.clean(folder, apply)

        if sub:
            for element in Path(folder).folders():
                self.clean(element, apply)
                self.move(element, apply)
                self.delete(element, apply)

    def clean(self, folder, apply):
        """Remove elements which match regex to be deleted"""
        for element in Path(folder).files():
            if self.is_to_delete(element):
                if apply:
                    os.remove(element)
                    logging.info(f"{element} deleted")
                else:
                    logging.info(f"{element} is candidate to deletion")

    def move(self, folder, apply):
        """Empty folder when no other files nor folders present"""
        path = Path(folder)

        if path.count() == 0 or len(path.folders()) > 0:
            return
        elements = path.files()
        total = path.count()
        videos = 0
        for element in elements:
            if self.__explorer.is_video(element):
                videos = videos + 1

        if videos == total:
            if apply:
                for element in elements:
                    current = Path(element)
                    if not pathlib.Path(f"{folder}{os.sep}..{os.sep}{current.name()}").exists():
                        current.move(f"..{os.sep}{current.name()}")
                if path.count() == 0:
                    logging.info(f"{folder} has been emptied")
                else:
                    logging.info(f"{folder} can't be emptied")
            else:
                logging.info(f"{folder} is candidate to simplification")

    def delete(self, folder, apply):
        """Delete folder when empty"""
        path = Path(folder)
        if path.count() == 0:
            self.__explorer.delete_folder(folder)

    def is_to_delete(self, element):
        for pattern in self.__to_delete:
            if re.search(pattern, element) is not None:
                return True
        return False
