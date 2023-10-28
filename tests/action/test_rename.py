import os
import unittest

from hcleanerlib.action.rename import Rename


class TestRename(unittest.TestCase):
    """Test for the Rename class."""

    def test_exec(self):
        """Test the exec method."""
        rename = Rename("test")
        path = ""

        self.assertTrue(os.path.exists(os.path.join(path, "[test] image.jpg")))

        expectation = {os.path.join(path, "[test] image.jpg"): os.path.join(path, "image.jpg")}
        result = rename.exec(path, False)

        self.assertEqual(expectation, result["changed"])
        self.assertTrue(os.path.exists(os.path.join(path, "[test] image.jpg")))

        expectation = {os.path.join(path, "[test] image.jpg"): os.path.join(path, "image.jpg")}
        result = rename.exec(path, True)

        self.assertEqual(expectation, result["changed"])
        self.assertFalse(os.path.exists(os.path.join(path, "[test] image.jpg")))
        self.assertTrue(os.path.exists(os.path.join(path, "image.jpg")))
