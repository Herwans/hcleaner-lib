import hashlib
import json
import logging
import os
import pathlib
from PIL import Image

from hcleanerlib.utils.config import Configuration


class Explorer:
    def __init__(self, config_type):
        self.__config = Configuration(config_type)

    def is_image(self, image_path):
        image_extensions = self.__config.get_image_extensions()
        return os.path.splitext(image_path)[1].strip('.') in image_extensions

    def is_video(self, video_path):
        image_extensions = self.__config.get_videos_extensions()
        return os.path.splitext(video_path)[1].strip('.') in image_extensions

    def is_image_only(self, folder_path):
        for element in os.listdir(folder_path):
            if self.is_image(f"{folder_path}/{element}") is False and element != "meta.json":
                return False
        return True

    def is_video_only(self, folder_path):
        for element in os.listdir(folder_path):
            if self.is_video(f"{folder_path}/{element}") is False and element != "meta.json":
                return False
        return True

    @staticmethod
    def is_image_corrupted(image_path):
        try:
            Image.open(image_path).verify()
            return False
        except (IOError, SyntaxError) as e:
            logging.info(f"Image {image_path} is corrupted")
            return True

    def create_meta_file(self, folder, current_name, new_name):
        global metadata_path, element_type
        path = f"{folder}/{current_name}"
        if os.path.exists(path):
            if os.path.isfile(path):
                element_type = "file"
                metadata_path = f"{folder}/{self.calculate_file_hash(path)}.json"
                if os.path.exists(metadata_path):
                    logging.info("Updating meta file...")
                    with open(metadata_path, 'r') as f:
                        metadata = json.load(f)
                else:
                    logging.info("Creating meta file...")
                    metadata = {"original_name": current_name}
                metadata["new_name"] = new_name
            elif os.path.isdir(path):
                element_type = "folder"
                metadata_path = f"{folder}/{current_name}/meta.json"
                logging.info(metadata_path)
                if os.path.exists(metadata_path):
                    logging.info("Updating meta file...")
                    with open(metadata_path, 'r') as f:
                        metadata = json.load(f)
                else:
                    logging.info("Creating meta file...")
                    metadata = {"original_name": current_name}
                metadata["new_name"] = new_name
            with open(metadata_path, "w") as f:
                json.dump(metadata, f)
            logging.info("It's a " + element_type)

    @staticmethod
    def delete_folder(path):
        elements = os.listdir(path)
        to_delete = pathlib.Path(path)
        if len(elements) == 0:
            pathlib.Path.rmdir(to_delete)
            return True
        elif len(elements) == 1 and elements[0] == "meta.json":
            os.remove(path + "/meta.json")
            pathlib.Path.rmdir(to_delete)
            return True
        return False

    @staticmethod
    def calculate_file_hash(file_path, hash_algorithm='sha256'):
        try:
            with open(file_path, 'rb') as f:
                hasher = hashlib.new(hash_algorithm)
                while chunk := f.read(8192):
                    hasher.update(chunk)
                return hasher.hexdigest()
        except FileNotFoundError:
            return None
