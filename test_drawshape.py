
import unittest
from drawshape import DrawShape
from PIL import Image
from util import *
from rect import Rect
import timeit

"""
xxx: todo, test if average_color performs better on smaller images
"""

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
        rect = Rect.init_random(self.image.size)
        color = average_color(rect.coords(), self.ds.og_image)

        rect = self.ds.find_best_shape(tries=3)
        color = average_color(rect.coords(), self.ds.og_image)
        diff1 = self.ds.get_staged_diff(rect, color)
        self.assertTrue(diff1 < diff0)

    def test_find_best_mutate(self):
        diff = DrawShape.rmsdiff(self.ds.og_image, self.ds.image)

        rect = Rect.init_coords(self.image.size, [0,0,200,200])
        color = average_color(rect.coords(), self.ds.og_image)
        diff0 = self.ds.get_staged_diff(rect, color)

        print rect.coords()
        rect, color = self.ds.find_best_mutate(rect, tries=10)
        print "@"*10
        diff1 = self.ds.get_staged_diff(rect, color)
        print diff1, diff0
        self.assertTrue(diff1 <= diff0)

    def test_efficiency(self):
        # 16x faster cropping, then RMS compared to comparing 1600x1200 image
        tries = 200 
        print "*"*10
        print "RMS diff sans crop"
        start_time = timeit.default_timer()
        for i in range(tries):
            DrawShape.rmsdiff(self.ds.image, self.ds.og_image)
        print(timeit.default_timer() - start_time)

        print "*"*10
        print "RMS diff crop"
        start_time = timeit.default_timer()
        for i in range(tries):
            rect_coords = (0,0,100,100)
            art_img, og_img = self.ds.crop_b4_compare(rect_coords)
            DrawShape.rmsdiff(art_img, og_img)
        print(timeit.default_timer() - start_time)


    def test_stage_draw(self):
        rect = Rect(self.image.size)
        color = average_color(rect.coords(), self.ds.og_image)
        diff0 = DrawShape.rmsdiff(self.image, self.ds.image)
        diff1 = self.ds.get_staged_diff(rect, color)
        self.assertTrue(diff1 < diff0)


if __name__ == '__main__':
    unittest.main()