from hcleanerlib.utils.applier import Applier
from hcleanerlib.utils.path import Path


class Detect:
    """Detect when cleaned elements of the folder have the same name."""

    def __init__(self, config_type: str):
        self.__applier = Applier(config_type)

    def exec(self, source_folder_path: str):
        """Execute the class behavior."""
        source_folder = Path(source_folder_path)

        cleaned_folders: dict[str, list] = {}
        cleaned_files: dict[str, list] = {}
        duplicate_folders: dict[str, list] = {}
        duplicate_files: dict[str, list] = {}

        # Clean each folder and create a key values entry for each of them
        # The key is the cleaned name
        # Don't check yet if it has duplication
        for sub_folder in source_folder.folders(True):
            cleaned = self.__applier.apply_folder_rules(sub_folder)
            if cleaned not in cleaned_folders:
                cleaned_folders[cleaned] = []
            cleaned_folders[cleaned].append(sub_folder)

        # Do the same as the previous one, but with file
        for file in source_folder.files(True):
            cleaned = self.__applier.apply_file_rules(file)
            if cleaned not in cleaned_files:
                cleaned_files[cleaned] = []
            cleaned_files[cleaned].append(file)

        # Filter to get only duplicate folders
        for key, value in cleaned_folders.items():
            if len(value) > 1:
                duplicate_folders[key] = value

        for key, value in cleaned_files.items():
            if len(value) > 1:
                duplicate_files[key] = value

        return {"folders": duplicate_folders, "files": duplicate_files}
