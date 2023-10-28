import hashlib
import logging
import os
import pathlib
from PIL import Image

from hcleanerlib.utils.config import Configuration
from hcleanerlib.utils.path import Path


class Explorer:
    """Class to manage Explorer and file system relative methods."""

    def __init__(self, config_type):
        self.__config = Configuration(config_type)

    def dispatch(self, element: Path):
        """Dispatch elements to respective locations."""
        images_dst = self.__config.get_images_location()
        videos_dst = self.__config.get_videos_location()

        if self.is_image(element.fullpath()) or self.is_image_only(element.fullpath()):
            element.move(images_dst)
        elif self.is_video(element.fullpath()) or self.is_video_only(element.fullpath()):
            element.move(videos_dst)

    def is_image(self, image_path):
        """Check if an element is an image"""
        image_extensions = self.__config.get_image_extensions()
        return os.path.splitext(image_path)[1].strip(".") in image_extensions

    def is_video(self, video_path):
        """Check if an element is a video"""
        image_extensions = self.__config.get_videos_extensions()
        return os.path.splitext(video_path)[1].strip(".") in image_extensions

    def is_image_only(self, folder_path: str):
        """Check if a folder contains only images"""
        try:
            for element in os.listdir(folder_path):
                if self.is_image(f"{folder_path}/{element}") is False:
                    return False
            return True
        except NotADirectoryError:
            return False

    def is_video_only(self, folder_path):
        """Check if a folder contains only videos"""
        try:
            for element in os.listdir(folder_path):
                if self.is_video(f"{folder_path}/{element}") is False:
                    return False
            return True
        except (FileNotFoundError, NotADirectoryError):
            return False

    @staticmethod
    def is_image_corrupted(image_path):
        """Check if image can be open"""
        try:
            Image.open(image_path).verify()
            return False
        except (IOError, SyntaxError):
            logging.info("Image %s is corrupted", image_path)
            return True

    @staticmethod
    def delete_folder(path):
        """Delete a folder"""
        elements = os.listdir(path)
        to_delete = pathlib.Path(path)
        if len(elements) == 0:
            pathlib.Path.rmdir(to_delete)
            return True
        if len(elements) == 1 and elements[0] == "meta.json":
            os.remove(path + "/meta.json")
            pathlib.Path.rmdir(to_delete)
            return True
        return False

    @staticmethod
    def calculate_file_hash(file_path, hash_algorithm="sha256"):
        """Calculate the file's hash"""
        try:
            with open(file_path, "rb") as f:
                hasher = hashlib.new(hash_algorithm)
                while chunk := f.read(8192):
                    hasher.update(chunk)
                return hasher.hexdigest()
        except FileNotFoundError:
            return None
