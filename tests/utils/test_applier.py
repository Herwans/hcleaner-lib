import unittest

from hcleanerlib.utils.applier import Applier
from hcleanerlib.utils.config import Configuration


class TestApplier(unittest.TestCase):
    def test_apply_file_rules(self):
        applier = Applier("test")
        text1 = "TODELETE My file2.mp4"
        self.assertEqual("My file2.mp4", applier.apply_file_rules(text1))

    def test_apply_folder_rules(self):
        applier = Applier("test")
        text1 = "[Prefix] Unknow 1 (testing) things to be sure -"
        self.assertEqual("Unknow 1 things to be sure", applier.apply_folder_rules(text1))

