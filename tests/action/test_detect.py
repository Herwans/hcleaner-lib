import unittest

from hcleanerlib.action.detect import Detect


class TestDetect(unittest.TestCase):
    def test_exec(self):
        detect = Detect("test")
        result = {
            "folders": {
                "1 2": [
                    "1 2 [test]",
                    "[test] 1 2"
                ]
            },
            "files": {
                "file 2.txt": [
                    "file 2 [test].txt",
                    "[test] file 2.txt"

                ]
            }
        }
        self.assertEqual(result, detect.exec("..\\sample"))
