import logging

from hcleanerlib.utils.applier import Applier
from hcleanerlib.utils.path import Path


class Detect:
    def __init__(self, config_type):
        self.__applier = Applier(config_type)

    def exec(self, folder):
        """Detect when elements have the same name after cleaning"""
        folder = Path(folder)

        duplicate_folders = {}
        duplicate_files = {}

        for sub_folder in folder.folders(True):
            cleaned = self.__applier.apply_folder_rules(sub_folder)
            if cleaned not in duplicate_folders.keys():
                duplicate_folders[cleaned] = []
            duplicate_folders[cleaned].append(sub_folder)

        for file in folder.files(True):
            cleaned = self.__applier.apply_file_rules(file)
            if cleaned not in duplicate_folders.keys():
                duplicate_folders[cleaned] = []
            duplicate_folders[cleaned].append(file)

        for title, elements in duplicate_folders.items():
            if len(elements) > 1:
                logging.warning(title)
                for element in elements:
                    logging.info("> " + element)

        for title, elements in duplicate_files.items():
            if len(elements) > 1:
                logging.warning(title)
                for element in elements:
                    logging.info("> " + element)
