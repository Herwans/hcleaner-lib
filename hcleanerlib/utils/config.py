import json
import pathlib


class Configuration:
    """Class which manage application configuration"""

    config_data = None

    def __init__(self, config_type):
        path = None
        default_path = pathlib.Path(f"{pathlib.Path.home()}/.horn/config.json")
        root_path = pathlib.Path("config.json")
        if default_path.exists() and default_path.is_file():
            path = default_path
        elif root_path.exists() and root_path.is_file():
            path = "config.json"

        if path is not None:
            with open(path, "r", encoding="UTF-8") as f:
                data = json.load(f)
                self.config_data = data[config_type]
        else:
            raise Exception("No rules found")

    def get_folder_rules(self):
        """Retrieve folders applicable rules"""
        return self.config_data["folder-rules"]

    def get_file_rules(self):
        """Retrieve files applicable rules"""
        return self.config_data["file-rules"]

    def get_extension_sets(self):
        """Retrieve the extensions sets"""
        return self.config_data["extension-set"]

    def get_image_extensions(self):
        """Get the extensions used for images"""
        return self.config_data["extensions"]["images"]

    def get_videos_extensions(self):
        """Get the extensions used for videos"""
        return self.config_data["extensions"]["videos"]

    def get_delete_pattern(self):
        """Get the pattern to delete"""
        return self.config_data["to-delete"]

    def get_videos_location(self):
        """Get the video's target location for dispatch"""
        return self.config_data["dispatch"]["videos"]

    def get_images_location(self):
        """Get the image's target location for dispatch"""
        return self.config_data["dispatch"]["images"]
