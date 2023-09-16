import os
import unittest

from hcleanerlib.utils.path import Path


class TestPath(unittest.TestCase):
    current_directory: str = os.getcwd()

    def test_init(self):
        original = "C:\\Windows\\System32"
        self.assertEqual(original, Path(original).fullpath())

    def test_init__not_exists(self):
        original = "C:\\ThisFolderShouldntExist\\"
        with self.assertRaises(FileNotFoundError):
            instance = Path(original)

    def test_fullpath__absolute_path(self):
        original = "C:\\Windows\\System32"
        self.assertEqual(original, Path(original).fullpath())

    def test_fullpath__relative_path(self):
        original = "existingFolder"
        os.mkdir(original)
        full = os.path.join(self.current_directory, original)
        self.assertEqual(full, Path(original).fullpath())
        os.rmdir(full)

    def test_fullpath__relative_path_back(self):
        original = "..\\utils"
        full = os.path.join(self.current_directory)
        self.assertEqual(full, Path(original).fullpath())

    def test_fullpath__relative_path_back_here(self):
        original = ".\\..\\utils"
        full = os.path.join(self.current_directory)
        self.assertEqual(full, Path(original).fullpath())

    def test_is_dir__dir(self):
        original = "C:\\Windows\\System32"
        self.assertTrue(Path(original).is_dir())

    def test_is_dir__file(self):
        original = "C:\\Windows\\System32\\bash.exe"
        self.assertFalse(Path(original).is_dir())

    def test_count(self):
        original = "."
        self.assertEqual(6, Path(original).count())

    def test_children(self):
        original = "."
        self.assertEqual(6, len(Path(original).children()))

    def test_files(self):
        original = "."
        self.assertEqual(5, len(Path(original).files()))

    def test_folders(self):
        original = "."
        self.assertEqual(1, len(Path(original).folders()))

    def test_move__file_absolute(self):
        absolute_src = os.path.join(os.getcwd(), "src", "file.txt")
        absolute_dir = os.path.join(os.getcwd(), "dst")
        absolute_dst = os.path.join(absolute_dir, "file.txt")
        os.mkdir("src")
        f = open(absolute_src, "a")
        f.write("test")
        f.close()
        file = Path(absolute_src)
        self.assertEqual(absolute_src, file.fullpath())
        self.assertTrue(os.path.exists(absolute_src))
        self.assertFalse(os.path.exists(absolute_dst))
        file.move(absolute_dir)
        self.assertEqual(absolute_dst, file.fullpath())
        self.assertTrue(os.path.exists(absolute_dst))
        self.assertFalse(os.path.exists(absolute_src))

    def test_move__file_relative_origin(self):
        absolute_src = os.path.join(os.getcwd(), "src2", "file.txt")
        absolute_dst = os.path.join(os.getcwd(), "src2\\dst2", "file.txt")
        dest = ".\\dst2"
        os.mkdir("src2")
        f = open(absolute_src, "a")
        f.write("test")
        f.close()
        file = Path(absolute_src)
        self.assertEqual(absolute_src, file.fullpath())
        self.assertTrue(os.path.exists(absolute_src))
        self.assertFalse(os.path.exists(absolute_dst))
        file.move(dest)
        self.assertEqual(absolute_dst, file.fullpath())
        self.assertTrue(os.path.exists(absolute_dst))
        self.assertFalse(os.path.exists(absolute_src))

    def test_move__file_relative_here(self):
        absolute_src = os.path.join(os.getcwd(), "src3", "file.txt")
        absolute_dst = os.path.join(os.getcwd(), "dst3", "file.txt")
        dest = "..\\dst3"
        os.mkdir("src3")
        f = open(absolute_src, "a")
        f.write("test")
        f.close()
        file = Path(absolute_src)
        self.assertEqual(absolute_src, file.fullpath())
        self.assertTrue(os.path.exists(absolute_src))
        self.assertFalse(os.path.exists(dest))
        file.move(dest)
        self.assertEqual(absolute_dst, file.fullpath())
        self.assertTrue(os.path.exists(absolute_dst))
        self.assertFalse(os.path.exists(absolute_src))

    def test_move__folder(self):
        absolute_src = os.path.join(os.getcwd(), "src4", "folder")
        absolute_dst = os.path.join(os.getcwd(), "dst4", "folder")
        dest = "..\\dst4"
        os.makedirs(absolute_src, exist_ok=True)
        file = Path(absolute_src)
        self.assertEqual(absolute_src, file.fullpath())
        self.assertTrue(os.path.exists(absolute_src))
        self.assertFalse(os.path.exists(absolute_dst))
        file.move(dest)
        self.assertEqual(absolute_dst, file.fullpath())
        self.assertTrue(os.path.exists(absolute_dst))
        self.assertFalse(os.path.exists(absolute_src))

    def test_move__folder_with_content(self):
        absolute_src = os.path.join(os.getcwd(), "src5", "folder")
        absolute_src_file = os.path.join(absolute_src, "file.txt")
        absolute_dst = os.path.join(os.getcwd(), "dst5", "folder")
        dest = "..\\dst5"
        os.makedirs(absolute_src, exist_ok=True)
        f = open(absolute_src_file, "a")
        f.write("test")
        f.close()
        file = Path(absolute_src)
        self.assertEqual(absolute_src, file.fullpath())
        self.assertTrue(os.path.exists(absolute_src))
        self.assertFalse(os.path.exists(absolute_dst))
        file.move(dest)
        self.assertEqual(absolute_dst, file.fullpath())
        self.assertTrue(os.path.exists(absolute_dst))
        self.assertFalse(os.path.exists(absolute_src))

    def test_move__already_exists(self):
        dst = "..\\dst6"
        absolute_src = os.path.join(os.getcwd(), "src6", "file.txt")
        absolute_dst = os.path.join(os.getcwd(), "dst6", "file.txt")
        os.mkdir("src6")
        os.mkdir("dst6")

        f = open(absolute_src, "a")
        f.write("test")
        f.close()

        f1 = open(absolute_dst, "a")
        f1.write("test2")
        f1.close()

        file = Path(absolute_src)
        self.assertEqual(absolute_src, file.fullpath())
        self.assertTrue(os.path.exists(absolute_src))
        self.assertTrue(os.path.exists(absolute_dst))

        with self.assertRaises(FileExistsError):
            file.move(dst)

        self.assertTrue(os.path.exists(absolute_src))
        self.assertTrue(os.path.exists(absolute_dst))


if __name__ == '__main__':
    unittest.main()

