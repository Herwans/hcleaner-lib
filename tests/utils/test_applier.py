import unittest

from hcleanerlib.utils.applier import Applier


class TestApplier(unittest.TestCase):
    """Test the Applier class"""

    def test_apply_file_rules(self):
        """Test if applier on files"""
        applier = Applier("test")
        text1 = "TODELETE My file2.mp4"
        self.assertEqual("My file2.mp4", applier.apply_file_rules(text1))

    def test_apply_folder_rules(self):
        """Test if applier on folders"""
        applier = Applier("test")
        text1 = "[Prefix] Unknown folder (testing) things to be sure -"
        self.assertEqual("Unknown folder things to be sure", applier.apply_folder_rules(text1))
