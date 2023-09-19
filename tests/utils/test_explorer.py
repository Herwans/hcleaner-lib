import os
import unittest

from hcleanerlib.utils.explorer import Explorer
from hcleanerlib.utils.path import Path


class TestExplorer(unittest.TestCase):
    def test_is_image__True(self):
        explorer = Explorer("test")
        self.assertTrue(explorer.is_image("C:\\Windows\\System32\\DefaultAccountTile.png"))

    def test_is_image__False(self):
        explorer = Explorer("test")
        self.assertFalse(explorer.is_image("C:\\Windows\\System32\\msdxm.tlb"))

    def test_is_video__True(self):
        explorer = Explorer("test")
        self.assertTrue(explorer.is_video("D:\\test\\test.mp4"))

    def test_is_video__False(self):
        explorer = Explorer("test")
        self.assertFalse(explorer.is_video("C:\\Windows\\System32\\DefaultAccountTile.png"))

    def test_is_image_only(self):
        explorer = Explorer("test")
        self.assertTrue(explorer.is_image_only("D:\\tests\\images"))

    def test_is_image_only__mixed(self):
        explorer = Explorer("test")
        self.assertFalse(explorer.is_image_only("D:\\tests\\mixed"))

    def test_is_image_only__video(self):
        explorer = Explorer("test")
        self.assertFalse(explorer.is_image_only("D:\\tests\\videos"))

    def test_is_image_only__not_folder(self):
        explorer = Explorer("test")
        self.assertFalse(explorer.is_image_only("D:\\tests\\test.jpg"))

    def test_is_image_only__not_found(self):
        explorer = Explorer("test")
        self.assertFalse(explorer.is_video_only("D:\\tests\\afazfaf"))

    def test_is_video_only(self):
        explorer = Explorer("test")
        self.assertTrue(explorer.is_video_only("D:\\tests\\videos"))

    def test_is_video_only__mixed(self):
        explorer = Explorer("test")
        self.assertFalse(explorer.is_video_only("D:\\tests\\mixed"))

    def test_is_video_only__video(self):
        explorer = Explorer("test")
        self.assertFalse(explorer.is_video_only("D:\\test\\images"))

    def test_is_video_only__not_folder(self):
        explorer = Explorer("test")
        self.assertFalse(explorer.is_video_only("D:\\tests\\test.mp4"))

    def test_is_video_only__not_found(self):
        explorer = Explorer("test")
        self.assertFalse(explorer.is_video_only("D:\\tests\\afazfd"))

    def test_dispatch(self):
        explorer = Explorer("test")
        to_dispatch = Path("D:\\tests\\to_dispatch")
        self.assertEqual(4, len(to_dispatch.children()))
        self.assertEqual(3, len(to_dispatch.files()))
        self.assertEqual(1, len(to_dispatch.folders()))
        self.assertEqual(4, to_dispatch.count())
        for element in to_dispatch.children():
            explorer.dispatch(Path(element))
        self.assertEqual(0, to_dispatch.count())
        self.assertEqual(3, len(os.listdir("D:\\tests\\images_target")))
        self.assertEqual(1, len(os.listdir("D:\\tests\\videos_target")))
