import os

from hcleanerlib.utils.applier import Applier
from hcleanerlib.utils.explorer import Explorer
from hcleanerlib.utils.path import Path


class Rename:
    """Allow to clean 1 elements' name"""
    def __init__(self, config_type):
        self.__applier = Applier(config_type)
        self.__explorer = Explorer(config_type)

    def exec(self, source_folder_path, apply=False):
        source_folder = Path(source_folder_path)

        result = {
            "changed": {},
            "skipped": [],
            "error": [],
            "ignore": []
        }

        for current_file in source_folder.files(True):
            new_file_name = self.__applier.apply_file_rules(current_file)

            path = os.path.join(source_folder.fullpath(), current_file)
            new_path = os.path.join(source_folder_path, new_file_name)

            if os.path.exists(new_path):
                result["skipped"].append(path)
            elif new_file_name != current_file:
                result["changed"][path] = new_path

        for subdirectory in source_folder.folders(True):
            new_folder_name = self.__applier.apply_folder_rules(subdirectory)
            path = os.path.join(source_folder.fullpath(), subdirectory)
            new_path = os.path.join(source_folder.fullpath(), new_folder_name)

            if os.path.exists(new_path):
                result["skipped"].append(path)
            elif path != new_path:
                result["changed"][path] = new_path

        if apply:
            for old, new in result["changed"].items():
                os.rename(old, new)
                if os.path.exists(old) or os.path.exists(new) is False:
                    result["error"].append(old)
                    result["changed"].pop(old)

        return result
