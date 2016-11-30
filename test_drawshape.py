
import unittest
from drawshape import DrawShape
from PIL import Image
from util import *
from rect import Rect
import timeit

class TestDrawShape(unittest.TestCase):

    def setUp(self):
        self.image = Image.open("pier.JPG")
        self.ds = DrawShape("pier.JPG")

    def tearDown(self):
        pass
    
    @classmethod
    def setUpClass(cls):
        """ get_some_resource() is slow, to avoid calling it for each test use setUpClass()
            and store the result as class variable
        """
        pass

    def test_crop_b4_compare(self):
        rect_coords = (0,0,100,100)
        art_img, og_img = self.ds.crop_b4_compare(rect_coords)
        self.assertEqual(art_img.size, og_img.size)

    def test_get_staged_diff(self):
        rect_coords = [0,0,100,100]
        rect = Rect.init_coords(rect_coords, rect_coords)
        diff = self.ds.get_staged_diff(rect, average_color(rect_coords, self.ds.og_image))
        self.assertEqual(diff, 102.82007830226222)

    def test_find_best_alpha(self):
        rect = Rect(self.image.size)
        r,g,b = average_color(rect.coords(), self.ds.og_image)
        color = (r,g,b,10)

        diff0 = self.ds.get_staged_diff(rect, color)
        color = self.ds.find_best_alpha(rect, tries=3)
        diff1 = self.ds.get_staged_diff(rect, color)
        
        self.assertTrue(diff1 < diff0)

    def test_find_best_shape(self):
        diff0 = DrawShape.rmsdiff(self.ds.og_image, self.ds.image)
        rect = Rect(self.image.size)
        color = average_color(rect.coords(), self.ds.og_image)
        # diff0 = self.ds.get_staged_diff(rect, color)

        rect = self.ds.find_best_shape(tries=3)
        color = average_color(rect.coords(), self.ds.og_image)
        diff1 = self.ds.get_staged_diff(rect, color)
        self.assertTrue(diff1 < diff0)

    def test_find_best_mutate(self):
        diff = DrawShape.rmsdiff(self.ds.og_image, self.ds.image)

        rect = Rect.init_coords(self.image.size, [0,0,200,200])
        color = average_color(rect.coords(), self.ds.og_image)
        diff0 = self.ds.get_staged_diff(rect, color)

        start_time = timeit.default_timer()
        print rect.coords()
        rect, color = self.ds.find_best_mutate(rect, tries=3)
        print "@"*10
        print(timeit.default_timer() - start_time)
        diff1 = self.ds.get_staged_diff(rect, color)
        print diff1, diff0
        self.assertTrue(diff1 < diff0)


    def test_stage_draw(self):
        rect = Rect(self.image.size)
        color = average_color(rect.coords(), self.ds.og_image)
        diff0 = DrawShape.rmsdiff(self.image, self.ds.image)
        diff1 = self.ds.get_staged_diff(rect, color)
        self.assertTrue(diff1 < diff0)


if __name__ == '__main__':
    unittest.main()