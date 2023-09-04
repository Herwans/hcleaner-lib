import shutil

from hcleanerlib.utils.explorer import Explorer
from hcleanerlib.utils.path import Path


class Simplify:
    def __init__(self, config_type):
        self.__explorer = Explorer(config_type)

    def exec(self, folder, apply, sub):
        """Remove empty folders, delete unwanted elements"""

        self.execute(folder, apply)

        if sub:
            for element in Path(folder).folders():
                self.execute(element, apply)

    def execute(self, folder, apply):
        """When a folder contains only a subfolder with the same name, move the subfolder's content"""
        folder = Path(folder)
        if folder.count() == 1 and len(folder.folders()) == 1:
            subfolder = Path(folder.folders()[0])
            if subfolder.name() == folder.name() and apply:
                for element in subfolder.files():
                    shutil.move(element, folder.fullpath())
                for element in subfolder.folders():
                    shutil.move(element, folder.fullpath())
                self.delete(subfolder.fullpath())

    def delete(self, folder):
        """Delete folder when empty"""
        path = Path(folder)
        if path.count() == 0:
            self.__explorer.delete_folder(folder)
