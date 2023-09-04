import logging
import os

from hcleanerlib.utils.applier import Applier
from hcleanerlib.utils.explorer import Explorer
from hcleanerlib.utils.path import Path


class Rename:
    def __init__(self, config_type):
        self.__applier = Applier(config_type)
        self.__explorer = Explorer(config_type)

    def exec(self, folder, apply, meta, no_meta, delete):
        """Allow to clean folder elements' name"""
        logging.info(f"{folder} folder content will be clean")
        current = Path(folder)
        logging.info(f"{current.count()} elements have been found")

        change = 0
        skip = 0
        error = 0
        delete_fail = []
        ignore = 0
        remove = 0

        for file in current.files(True):
            if os.path.splitext(file)[1] == ".json":
                ignore = ignore + 1
                continue

            new_file_name = self.__applier.apply_file_rules(file)

            path = f"{folder}/{file}"
            new_path = f"{folder}/{new_file_name}"

            if os.path.exists(new_path):
                skip = skip + 1
            elif new_file_name != file:
                logging.info("=====================")
                logging.info("Old : \t" + file)
                logging.info("New : \t" + new_file_name)

                if apply:
                    os.rename(path, new_path)
                    if os.path.exists(path) is False and os.path.exists(new_path):
                        change = change + 1
                    else:
                        error = error + 1
            if (apply and not no_meta) or meta:
                self.__explorer.create_meta_file(folder, file, new_file_name)

        for fol in current.folders(True):
            if apply and delete and self.__explorer.delete_folder(fol):
                remove = remove + 1
                continue

            new_folder_name = self.__applier.apply_folder_rules(fol)
            path = f"{folder}/{fol}"
            new_path = f"{folder}/{new_folder_name}"

            if os.path.exists(new_path):
                skip = skip + 1
            elif new_folder_name != fol:
                logging.info("=====================")
                logging.info("Old : \t" + fol)
                logging.info("New : \t" + new_folder_name)

                if apply:
                    os.rename(path, new_path)
                    if os.path.exists(path) is False and os.path.exists(new_path):
                        change = change + 1
                    else:
                        error = error + 1
            if apply or meta:
                self.__explorer.create_meta_file(folder, fol, new_folder_name)

        logging.info(f"{change} element(s) changed")
        logging.info(f"{skip} element(s) skipped")
        logging.info(f"{remove} element(s) deleted")
        logging.info(f"{error} element(s) failed")
        logging.info(f"{ignore} element(s) ignored")
        if len(delete_fail) > 0:
            logging.info("The following folders couldn't be deleted")
            print(delete_fail)

        return
