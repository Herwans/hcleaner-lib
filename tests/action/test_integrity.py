import os
import unittest

from hcleanerlib.action.integrity import Integrity


class TestIntegrity(unittest.TestCase):
    def test_exec(self):
        integrity = Integrity("test")
        path = ""

        # Recursive, dry run
        self.assertTrue(os.path.exists(os.path.join(path, "1", "1.jpg")))
        self.assertTrue(os.path.exists(os.path.join(path, "1", "2.jpg")))
        self.assertTrue(os.path.exists(os.path.join(path, "2", "1.jpg")))
        self.assertTrue(os.path.exists(os.path.join(path, "2", "2.jpg")))
        self.assertTrue(os.path.exists(os.path.join(path, "3", "1.jpg")))
        self.assertTrue(os.path.exists(os.path.join(path, "3", "2.jpg")))

        result = integrity.exec(path, False, True)

        self.assertTrue({os.path.join(path, "1"): "0", os.path.join(path, "2"): "50", os.path.join(path, "3"): "100"}, result)

        self.assertTrue(os.path.exists(os.path.join(path, "1", "1.jpg")))
        self.assertTrue(os.path.exists(os.path.join(path, "1", "2.jpg")))
        self.assertTrue(os.path.exists(os.path.join(path, "2", "1.jpg")))
        self.assertTrue(os.path.exists(os.path.join(path, "2", "2.jpg")))
        self.assertTrue(os.path.exists(os.path.join(path, "3", "1.jpg")))
        self.assertTrue(os.path.exists(os.path.join(path, "3", "2.jpg")))

        result = integrity.exec(path, True, True)
        self.assertTrue({os.path.join(path, "1"): "0", os.path.join(path, "2"): "50", os.path.join(path, "3"): "100"},
                        result)

        self.assertTrue(os.path.exists(os.path.join(path, "1", "1.jpg")))
        self.assertTrue(os.path.exists(os.path.join(path, "1", "2.jpg")))
        self.assertTrue(os.path.exists(os.path.join(path, "2", "1.jpg")))
        self.assertTrue(os.path.exists(os.path.join(path, "2", "2.jpg")))
        self.assertFalse(os.path.exists(os.path.join(path, "3", "1.jpg")))
        self.assertFalse(os.path.exists(os.path.join(path, "3", "2.jpg")))


