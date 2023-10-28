import os
import unittest

from hcleanerlib.utils.path import Path


class TestPath(unittest.TestCase):
    """Test the Path class."""

    current_directory: str = os.getcwd()

    def test_init(self):
        """Test the init method of the class."""
        original = "C:\\Windows\\System32"
        self.assertEqual(original, Path(original).fullpath())

    def test_init__not_exists(self):
        """Test if an error is raised when invalid path is passed to init."""
        original = "C:\\ThisFolderShouldntExist\\"
        with self.assertRaises(FileNotFoundError):
            Path(original)

    def test_fullpath__absolute_path(self):
        """Test the fullpath method."""
        original = "C:\\Windows\\System32"
        self.assertEqual(original, Path(original).fullpath())

    def test_fullpath__relative_path(self):
        """Test the fullpath method when relative pass is given in the init."""
        original = "existingFolder"
        os.mkdir(original)
        full = os.path.join(self.current_directory, original)
        self.assertEqual(full, Path(original).fullpath())
        os.rmdir(full)

    def test_fullpath__relative_path_back(self):
        """Test the fullpath method when relative pass is given in the init
        with back track."""
        original = "..\\utils"
        full = os.path.join(self.current_directory)
        self.assertEqual(full, Path(original).fullpath())

    def test_fullpath__relative_path_back_here(self):
        """Test the fullpath method when relative pass is given in the init
        with back track and current location."""
        original = ".\\..\\utils"
        full = os.path.join(self.current_directory)
        self.assertEqual(full, Path(original).fullpath())

    def test_is_folder__folder(self):
        """Test that folder checker works."""
        original = "C:\\Windows\\System32"
        self.assertTrue(Path(original).is_folder())

    def test_is_folder__file(self):
        """Test that a file is not detected as a folder."""
        original = "C:\\Windows\\System32\\bash.exe"
        self.assertFalse(Path(original).is_folder())

    def test_count(self):
        """Test that count returns the right amount of elements."""
        original = "."
        self.assertEqual(5, Path(original).count())

    def test_children(self):
        """Test that all children of the path are returned."""
        original = "."
        self.assertEqual(5, len(Path(original).children()))

    def test_files(self):
        """Test that all files of the path are returned."""
        original = "."
        self.assertEqual(4, len(Path(original).files()))

    def test_folders(self):
        """Test that all folders of the path are returned."""
        original = "."
        self.assertEqual(1, len(Path(original).folders()))

    def test_move__file_absolute(self):
        """Test that a file can be moved to another location."""
        absolute_src = os.path.join(os.getcwd(), "src", "file.txt")
        absolute_dir = os.path.join(os.getcwd(), "dst")
        absolute_dst = os.path.join(absolute_dir, "file.txt")
        os.mkdir("src")
        with open(absolute_src, "a", encoding="UTF-8") as f:
            f.write("test")
        file = Path(absolute_src)
        self.assertEqual(absolute_src, file.fullpath())
        self.assertTrue(os.path.exists(absolute_src))
        self.assertFalse(os.path.exists(absolute_dst))
        file.move(absolute_dir)
        self.assertEqual(absolute_dst, file.fullpath())
        self.assertTrue(os.path.exists(absolute_dst))
        self.assertFalse(os.path.exists(absolute_src))

    def test_move__file_relative_origin(self):
        """Test that a file can be moved to another location using relative location."""
        absolute_src = os.path.join(os.getcwd(), "src2", "file.txt")
        absolute_dst = os.path.join(os.getcwd(), "src2\\dst2", "file.txt")
        dst = ".\\dst2"
        os.mkdir("src2")
        with open(absolute_src, "a", encoding="UTF-8") as f:
            f.write("test")
        file = Path(absolute_src)
        self.assertEqual(absolute_src, file.fullpath())
        self.assertTrue(os.path.exists(absolute_src))
        self.assertFalse(os.path.exists(absolute_dst))
        file.move(dst)
        self.assertEqual(absolute_dst, file.fullpath())
        self.assertTrue(os.path.exists(absolute_dst))
        self.assertFalse(os.path.exists(absolute_src))

    def test_move__file_relative_here(self):
        """Test that a file can be moved to another location using relative location."""
        absolute_src = os.path.join(os.getcwd(), "src3", "file.txt")
        absolute_dst = os.path.join(os.getcwd(), "dst3", "file.txt")
        dst = "..\\dst3"
        os.mkdir("src3")
        with open(absolute_src, "a", encoding="UTF-8") as f:
            f.write("test")
        file = Path(absolute_src)
        self.assertEqual(absolute_src, file.fullpath())
        self.assertTrue(os.path.exists(absolute_src))
        self.assertFalse(os.path.exists(dst))
        file.move(dst)
        self.assertEqual(absolute_dst, file.fullpath())
        self.assertTrue(os.path.exists(absolute_dst))
        self.assertFalse(os.path.exists(absolute_src))

    def test_move__folder(self):
        """Test that a folder can be moved to another location."""
        absolute_src = os.path.join(os.getcwd(), "src4", "1")
        absolute_dst = os.path.join(os.getcwd(), "dst4", "1")
        dst = "..\\dst4"
        os.makedirs(absolute_src, exist_ok=True)
        file = Path(absolute_src)
        self.assertEqual(absolute_src, file.fullpath())
        self.assertTrue(os.path.exists(absolute_src))
        self.assertFalse(os.path.exists(absolute_dst))
        file.move(dst)
        self.assertEqual(absolute_dst, file.fullpath())
        self.assertTrue(os.path.exists(absolute_dst))
        self.assertFalse(os.path.exists(absolute_src))

    def test_move__folder_with_content(self):
        """Test that a folder with content can be moved to another location."""
        absolute_src = os.path.join(os.getcwd(), "src5", "1")
        absolute_src_file = os.path.join(absolute_src, "file.txt")
        absolute_dst = os.path.join(os.getcwd(), "dst5", "1")
        dst = "..\\dst5"
        os.makedirs(absolute_src, exist_ok=True)
        with open(absolute_src_file, "a", encoding="UTF-8") as f:
            f.write("test")
        file = Path(absolute_src)
        self.assertEqual(absolute_src, file.fullpath())
        self.assertTrue(os.path.exists(absolute_src))
        self.assertFalse(os.path.exists(absolute_dst))
        file.move(dst)
        self.assertEqual(absolute_dst, file.fullpath())
        self.assertTrue(os.path.exists(absolute_dst))
        self.assertFalse(os.path.exists(absolute_src))

    def test_move__already_exists(self):
        """Test that moving an element to a location
        where another element with same name already exists
        throw an exception."""

        dst = "..\\dst6"
        absolute_src = os.path.join(os.getcwd(), "src6", "file.txt")
        absolute_dst = os.path.join(os.getcwd(), "dst6", "file.txt")
        os.mkdir("src6")
        os.mkdir("dst6")

        with open(absolute_src, "a", encoding="UTF-8") as f:
            f.write("test")

        with open(absolute_dst, "a", encoding="UTF-8") as f1:
            f1.write("test2")

        file = Path(absolute_src)
        self.assertEqual(absolute_src, file.fullpath())
        self.assertTrue(os.path.exists(absolute_src))
        self.assertTrue(os.path.exists(absolute_dst))

        with self.assertRaises(FileExistsError):
            file.move(dst)

        self.assertTrue(os.path.exists(absolute_src))
        self.assertTrue(os.path.exists(absolute_dst))


if __name__ == "__main__":
    unittest.main()
