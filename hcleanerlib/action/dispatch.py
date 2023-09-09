import logging
import shutil
from os import sep

from hcleanerlib.utils.explorer import Explorer
from hcleanerlib.utils.path import Path


class Dispatch:
    def __init__(self, config_type):
        self.__parent: Path = None
        self.__explorer = Explorer(config_type)

    def exec(self, folder, apply=False):
        current = Path(folder)
        for element in current.children():
            try:
                self.__explorer.dispatch(Path(f"{current.fullpath()}{sep}{element}"))
            except ValueError:
                logging.info(element + " skipped du to error")
                logging.info(ValueError)
