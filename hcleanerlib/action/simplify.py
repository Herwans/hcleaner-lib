import shutil

from hcleanerlib.utils.explorer import Explorer
from hcleanerlib.utils.path import Path


class Simplify:
    def __init__(self, config_type):
        self.__parent: Path = None
        self.__explorer = Explorer(config_type)

    def exec(self, folder, apply=False):
        """
        Crawl direct sub folders, extract videos when alone in folder, and remove empty folders.
        """

        self.__parent = Path(folder)
        for child_folder in self.__parent.folders():
            for log in self.__extract_folder(child_folder, apply):
                yield log
            for log in self.__extract_video(child_folder, apply):
                yield log
            for log in self.__delete_when_empty(child_folder, apply):
                yield log

    def __extract_video(self, folder, apply):
        current = Path(folder)
        if self.__explorer.is_video_only(current.fullpath()):
            if apply is False:
                yield current.name() + " is video only, it can be emptied"
            else:
                for video in current.files():
                    shutil.move(video, self.__parent.fullpath())
                    yield video + " has been moved to " + self.__parent.fullpath() + video

    def __extract_folder(self, folder, apply):
        current = Path(folder)
        if current.count() == 1 and len(current.folders()) == 1:
            if current.name() == Path(current.folders()[0]).name():
                if apply is False:
                    yield current.name() + " has a folder with the same name, it can be simplified"
                else:
                    Path(current.folders()[0]).move(self.__parent.fullpath())
                    yield current.name() + " has been moved into its parent"

    def __delete_when_empty(self, folder, apply):
        current = Path(folder)
        if current.count() == 0:
            if apply is False:
                yield current.name() + " is empty, can be delete"
            else:
                self.__explorer.delete_folder(current.fullpath())
                yield current.name() + " has been deleted"

