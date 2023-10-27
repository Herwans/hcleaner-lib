import os
import unittest

from hcleanerlib.action.simplify import Simplify


class TestSimplify(unittest.TestCase):
    def test_exec(self):
        simplify = Simplify("test")
        path = "D:\\dev\\herwans\\hcleaner-lib\\tests\\sample\\simplify"

        self.assertTrue(os.path.exists(os.path.join(path, "1")))
        self.assertTrue(os.path.exists(os.path.join(path, "1", "file.mp4")))
        self.assertTrue(os.path.exists(os.path.join(path, "2")))
        self.assertTrue(os.path.exists(os.path.join(path, "2", "file2.mp4")))
        self.assertTrue(os.path.exists(os.path.join(path, "2", "test.jpg")))
        self.assertTrue(os.path.exists(os.path.join(path, "folder")))
        self.assertTrue(os.path.exists(os.path.join(path, "folder", "folder")))
        self.assertTrue(os.path.exists(os.path.join(path, "folder", "folder", "thing.jpg")))

        # No apply
        expectation = {"extractable": [
            os.path.join(path, "1"),
            os.path.join(path, "folder")
        ], "extracted": [], "error": [], "deletable": [os.path.join(path, "1")], "deleted": [

        ]}
        result = simplify.exec(path, False)

        self.assertEqual(expectation, result)

        self.assertTrue(os.path.exists(os.path.join(path, "1")))
        self.assertTrue(os.path.exists(os.path.join(path, "1", "file.mp4")))
        self.assertTrue(os.path.exists(os.path.join(path, "2")))
        self.assertTrue(os.path.exists(os.path.join(path, "2", "file2.mp4")))
        self.assertTrue(os.path.exists(os.path.join(path, "2", "test.jpg")))
        self.assertTrue(os.path.exists(os.path.join(path, "folder")))
        self.assertTrue(os.path.exists(os.path.join(path, "folder", "folder")))
        self.assertTrue(os.path.exists(os.path.join(path, "folder", "folder", "thing.jpg")))

        # apply

        expectation = {
            "extractable": [],
            "extracted": [os.path.join(path, "file.mp4"), os.path.join(path, "folder")],
            "error": [],
            "deletable": [],
            "deleted": [
                os.path.join(path, "1")
            ]
        }
        result = simplify.exec(path, True)

        self.assertEqual(expectation, result)

        self.assertFalse(os.path.exists(os.path.join(path, "1")))
        self.assertTrue(os.path.exists(os.path.join(path, "file.mp4")))
        self.assertTrue(os.path.exists(os.path.join(path, "2")))
        self.assertTrue(os.path.exists(os.path.join(path, "2", "file2.mp4")))
        self.assertTrue(os.path.exists(os.path.join(path, "2", "test.jpg")))
        self.assertTrue(os.path.exists(os.path.join(path, "folder")))
        self.assertFalse(os.path.exists(os.path.join(path, "folder", "folder")))
        self.assertTrue(os.path.exists(os.path.join(path, "folder", "thing.jpg")))

