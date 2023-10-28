import unittest

from hcleanerlib.action.detect import Detect


class TestDetect(unittest.TestCase):
    """Test for the Detect class."""

    def test_exec(self):
        """Test the exec method."""
        detect = Detect("test")
        result = {
            "folders": {"folder 1": ["folder 1 [test]", "[test] folder 1"]},
            "files": {"file 1.txt": ["file 1 [test].txt", "[test] file 1.txt"]},
        }
        self.assertEqual(result, detect.exec("..\\sample\\detect"))
