from hcleanerlib.utils.explorer import Explorer
from hcleanerlib.utils.path import Path


class Simplify:
    """Crawl direct sub folders, extract videos when alone in folder, and remove empty folders."""

    def __init__(self, config_type):
        self.__source_folder = None
        self.__explorer = Explorer(config_type)

    def exec(self, source_folder_path: str, apply: bool = False):
        """Execute the class behavior."""
        result: dict[str, list] = {
            "extractable": [],
            "extracted": [],
            "error": [],
            "deletable": [],
            "deleted": [],
        }

        self.__source_folder = Path(source_folder_path)
        for subdirectory in self.__source_folder.folders():
            current = Path(subdirectory)
            if self.__explorer.is_video_only(current.fullpath()):
                if apply:
                    extracted, error = self.__extract_video(current)
                    result["extracted"] = result["extracted"] + extracted
                    result["error"] = result["error"] + error
                else:
                    result["extractable"].append(current.fullpath())
            elif self.__is_extractable_folder(current):
                if apply:
                    Path(current.folders()[0]).move(self.__source_folder.fullpath(), True)
                    result["extracted"].append(current.fullpath())
                else:
                    result["extractable"].append(current.fullpath())

            if current.count() == 0 or (
                self.__is_extractable_folder(current) is False
                and current.fullpath() in result["extractable"]
            ):
                if apply is False:
                    result["deletable"].append(current.fullpath())
                else:
                    self.__explorer.delete_folder(current.fullpath())
                    result["deleted"].append(current.fullpath())

        return result

    def __extract_video(self, current_folder: Path):
        extracted = []
        error = []
        for video in current_folder.files():
            v = Path(video)
            try:
                v.move(self.__source_folder.fullpath())
                extracted.append(v.fullpath())
            except FileNotFoundError:
                error.append(v.fullpath())

        return extracted, error

    @staticmethod
    def __is_extractable_folder(current_folder: Path):
        return (
            current_folder.count() == 1
            and len(current_folder.folders()) == 1
            and current_folder.name() == Path(current_folder.folders()[0]).name()
        )
