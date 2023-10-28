import os
import unittest

from hcleanerlib.action.dispatch import Dispatch


class TestDispatch(unittest.TestCase):
    """Test for the Dispatch class."""

    def test_exec(self):
        """Test the exec method."""
        dispatch = Dispatch("test")
        path = "..\\sample\\dispatch"

        self.assertTrue(os.path.exists(os.path.join(path, "src", "image.jpg")))
        self.assertTrue(os.path.exists(os.path.join(path, "src", "video.mp4")))
        self.assertTrue(os.path.exists(os.path.join(path, "src", "videos")))
        dispatch.exec(os.path.join(path, "src"))
        self.assertFalse(os.path.exists(os.path.join(path, "src", "image.jpg")))
        self.assertFalse(os.path.exists(os.path.join(path, "src", "video.mp4")))
        self.assertTrue(os.path.exists(os.path.join(path, "dst", "images", "image.jpg")))
        self.assertTrue(os.path.exists(os.path.join(path, "dst", "videos", "video.mp4")))
        self.assertTrue(os.path.exists(os.path.join(path, "dst", "videos", "videos")))
