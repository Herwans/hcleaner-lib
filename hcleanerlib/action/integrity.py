import json
import logging
import os
import pathlib
import shutil
from datetime import datetime

from hcleanerlib.utils.explorer import Explorer


class Integrity:
    def __init__(self, config_type):
        self.__explorer = Explorer(config_type)

    def exec(self, folder, delete, sub, verbose):
        """Check file integrity"""
        logging.info(f"{folder} folder content will be checked")

        if sub:
            for sub_folder in os.listdir(folder):
                path = f"{folder}/{sub_folder}"
                if os.path.isdir(path):
                    corrupted, total = self.check_folder_content(path, verbose)
                    if corrupted > 0:
                        logging.info(f"{sub_folder} contains {corrupted} corrupted images ({corrupted / total * 100}%)")
                        if delete and corrupted == total:
                            if self.delete_corrupted_folder(path, corrupted, total):
                                logging.info(f"{sub_folder} deleted")
                            else:
                                logging.info(f"{sub_folder} kept")
        else:
            corrupted, total = self.check_folder_content(folder, verbose)
            if corrupted > 0:
                logging.info(f"{folder} contains {corrupted} corrupted images ({corrupted / total * 100}%)")
                if delete and corrupted == total:
                    if self.delete_corrupted_folder(folder, corrupted, total):
                        logging.info(f"{folder} deleted")
                    else:
                        logging.info(f"{folder} kept")

        return

    def check_folder_content(self, folder, verbose):
        corrupted = 0
        total_files = 0
        for file in os.listdir(folder):
            if file == "meta.json":
                continue
            total_files = total_files + 1
            if self.__explorer.is_image(f"{folder}/{file}") and self.__explorer.is_image_corrupted(f"{folder}/{file}",
                                                                                                   verbose):
                corrupted = corrupted + 1

        return corrupted, total_files

    def delete_corrupted_folder(self, folder, corrupted, total):
        for element in os.listdir(folder):
            if element != "meta.json" and self.__explorer.is_image(element) is False and os.path.isfile(
                    element) is False:
                logging.info(element)
                return False
        meta = f"{folder}/meta.json"
        metas = f"{pathlib.Path.home()}/.horn/meta_delete.json"

        if os.path.exists(metas):
            with open(metas, 'r') as f:
                metadatas = json.load(f)
        else:
            metadatas = []

        if os.path.exists(meta):
            with open(meta, 'r') as f:
                metadata = json.load(f)
        else:
            metadata = {"original_name": folder}

        metadata["corruption"] = corrupted / total * 100
        metadata["deleted_at"] = datetime.now().__str__()

        metadatas.append(metadata)
        with open(metas, "w") as f:
            json.dump(metadatas, f)

        shutil.rmtree(folder)
        return True