import logging
import shutil
from os import sep

from hcleanerlib.utils.explorer import Explorer
from hcleanerlib.utils.path import Path


class Dispatch:
    def __init__(self, config_type):
        self.__parent = None
        self.__explorer = Explorer(config_type)

    def exec(self, folder):
        current = Path(folder)
        for element in current.children():
            try:
                self.__explorer.dispatch(Path(element))
            except ValueError:
                logging.info(element + " skipped du to error")
                logging.info(ValueError)
