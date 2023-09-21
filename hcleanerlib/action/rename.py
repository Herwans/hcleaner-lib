import os

from hcleanerlib.utils.applier import Applier
from hcleanerlib.utils.explorer import Explorer
from hcleanerlib.utils.path import Path


class Rename:
    def __init__(self, config_type):
        self.__applier = Applier(config_type)
        self.__explorer = Explorer(config_type)

    def exec(self, folder, apply=False):
        """Allow to clean folder elements' name"""
        yield f"Folder to clean: {folder}"
        current = Path(folder)
        yield f"Elements found in the folder: {current.count()}"
        yield f" Files: {len(current.files())}"
        yield f" Folders: {len(current.folders())}"

        change = 0
        skip = 0
        error = 0
        ignore = 0

        for file in current.files(True):
            new_file_name = self.__applier.apply_file_rules(file)

            path = os.path.join(folder, file)
            new_path = os.path.join(folder, new_file_name)

            if os.path.exists(new_path):
                skip = skip + 1
            elif new_file_name != file:
                yield "====================="
                yield "Old : \t" + file
                yield "New : \t" + new_file_name

                if apply:
                    os.rename(path, new_path)
                    if os.path.exists(path) is False and os.path.exists(new_path):
                        change = change + 1
                    else:
                        error = error + 1

        for fol in current.folders(True):

            new_folder_name = self.__applier.apply_folder_rules(fol)
            path = f"{folder}/{fol}"
            new_path = f"{folder}/{new_folder_name}"

            if os.path.exists(new_path):
                skip = skip + 1
            elif new_folder_name != fol:
                yield "====================="
                yield "Old : \t" + fol
                yield "New : \t" + new_folder_name

                if apply:
                    os.rename(path, new_path)
                    if os.path.exists(path) is False and os.path.exists(new_path):
                        change = change + 1
                    else:
                        error = error + 1

        yield f"{change} element(s) changed"
        yield f"{skip} element(s) skipped"
        yield f"{error} element(s) failed"
        yield f"{ignore} element(s) ignored"

        return
