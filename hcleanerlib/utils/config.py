import json
import pathlib


class Configuration:
    configData = None

    def __init__(self, config_type):
        path = None
        default_path = pathlib.Path(f"{pathlib.Path.home()}/.horn/config.json")
        root_path = pathlib.Path("config.json")
        if default_path.exists() and default_path.is_file():
            path = default_path
        elif root_path.exists() and root_path.is_file():
            path = "config.json"

        if path is not None:
            with open(path, 'r') as f:
                data = json.load(f)
                self.configData = data[config_type]
        else:
            Exception("No rules found")

    def get_folder_rules(self):
        return self.configData['folder-rules']

    def get_file_rules(self):
        return self.configData['file-rules']

    def get_extension_sets(self):
        return self.configData['extension-set']

    def get_image_extensions(self):
        return self.configData["extensions"]["images"]

    def get_videos_extensions(self):
        return self.configData["extensions"]["videos"]

    def get_delete_pattern(self):
        return self.configData["to-delete"]

    def get_videos_location(self):
        return self.configData["dispatch"]["videos"]

    def get_images_location(self):
        return self.configData["dispatch"]["images"]

