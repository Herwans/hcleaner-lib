import os
import unittest

from hcleanerlib.action.garbage import Garbage


class TestGarbage(unittest.TestCase):
    def test_exec(self):
        garbage = Garbage("test")
        path = ""

        # No recursive, dry run
        self.assertTrue(os.path.exists(os.path.join(path, "info.nfo")))
        self.assertTrue(os.path.exists(os.path.join(path, "1.jpg")))
        self.assertTrue(os.path.exists(os.path.join(path, "test.mht")))
        self.assertTrue(os.path.exists(os.path.join(path, "fol", "info.nfo")))
        self.assertTrue(os.path.exists(os.path.join(path, "fol", "1.jpg")))
        self.assertTrue(os.path.exists(os.path.join(path, "fol", "test.mht")))

        expect_result_1 = [os.path.join(path, "1.jpg"), os.path.join(path, "info.nfo"),
                                 os.path.join(path, "test.mht")]
        result_1 = garbage.exec(os.path.join(path))
        self.assertEqual(expect_result_1, result_1["to_delete"])

        # No recursive, apply
        self.assertTrue(os.path.exists(os.path.join(path, "info.nfo")))
        self.assertTrue(os.path.exists(os.path.join(path, "1.jpg")))
        self.assertTrue(os.path.exists(os.path.join(path, "test.mht")))
        self.assertTrue(os.path.exists(os.path.join(path, "fol", "info.nfo")))
        self.assertTrue(os.path.exists(os.path.join(path, "fol", "1.jpg")))
        self.assertTrue(os.path.exists(os.path.join(path, "fol", "test.mht")))

        expect_result_2 =[os.path.join(path, "1.jpg"), os.path.join(path, "info.nfo"),
                                  os.path.join(path, "test.mht")]
        self.assertEqual(expect_result_2, garbage.exec(os.path.join(path), True)["deleted"])

        self.assertFalse(os.path.exists(os.path.join(path, "info.nfo")))
        self.assertFalse(os.path.exists(os.path.join(path, "1.jpg")))
        self.assertFalse(os.path.exists(os.path.join(path, "test.mht")))

        # Recursive, dry run
        self.assertTrue(os.path.exists(os.path.join(path, "fol", "info.nfo")))
        self.assertTrue(os.path.exists(os.path.join(path, "fol", "1.jpg")))
        self.assertTrue(os.path.exists(os.path.join(path, "fol", "test.mht")))

        expect_result_3 = [os.path.join(path, "fol", "1.jpg"), os.path.join(path, "fol", "info.nfo"),
                                  os.path.join(path, "fol", "test.mht"), os.path.join(path, "fol")]

        self.assertEqual(expect_result_3, garbage.exec(os.path.join(path), False, True)["to_delete"])

        # Recursive, apply
        self.assertTrue(os.path.exists(os.path.join(path, "fol", "info.nfo")))
        self.assertTrue(os.path.exists(os.path.join(path, "fol", "1.jpg")))
        self.assertTrue(os.path.exists(os.path.join(path, "fol", "test.mht")))
        expect_result_4 = [os.path.join(path, "fol", "1.jpg"), os.path.join(path, "fol", "info.nfo"),
                                  os.path.join(path, "fol", "test.mht"), os.path.join(path, "fol")]

        self.assertEqual(expect_result_4, garbage.exec(os.path.join(path), True, True)["deleted"])
        self.assertFalse(os.path.exists(os.path.join(path, "fol", "info.nfo")))
        self.assertFalse(os.path.exists(os.path.join(path, "fol", "1.jpg")))
        self.assertFalse(os.path.exists(os.path.join(path, "fol", "test.mht")))
        self.assertFalse(os.path.exists(os.path.join(path, "fol")))
