import logging

from hcleanerlib.utils.explorer import Explorer
from hcleanerlib.utils.path import Path


class Dispatch:
    """Move elements on a specific folder which match with them."""

    def __init__(self, config_type: str):
        self.__explorer = Explorer(config_type)

    def exec(self, source_folder_path: str):
        """Execute the class behavior."""
        source_folder = Path(source_folder_path)
        for element in source_folder.children():
            try:
                self.__explorer.dispatch(Path(element))
            except ValueError:
                logging.info("%s skipped du to error", element)
                logging.info(ValueError)
