import unittest

from hcleanerlib.utils.applier import Applier
from hcleanerlib.utils.config import Configuration


class TestApplier(unittest.TestCase):
    def test_apply_file_rules(self):
        applier = Applier("test")
        text1 = "TODELETE My file.mp4"
        self.assertEqual("My file.mp4", applier.apply_file_rules(text1))

    def test_apply_folder_rules(self):
        applier = Applier("test")
        text1 = "[Prefix] Unknow folder (testing) things to be sure -"
        self.assertEqual("Unknow folder things to be sure", applier.apply_folder_rules(text1))

