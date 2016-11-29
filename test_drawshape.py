
import unittest
from drawshape import DrawShape
from PIL import Image
from util import *
from rect import Rect

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
        rect_coords = ((0,0), (100,100))
        art_img, og_img = self.ds.crop_b4_compare(rect_coords)
        self.assertEqual(art_img.size, og_img.size)
        

    def test_find_best_alpha(self):
        diff = DrawShape.rmsdiff(self.ds.og_image, self.ds.image)
        rect = Rect(self.image.size)
        r,g,b = average_color(rect, self.ds.og_image)
        color = (r,g,b,10)

        staged_image = self.ds.stage_draw(rect, color=color)
        diff0 = DrawShape.rmsdiff(self.ds.og_image, staged_image)


        color = self.ds.find_best_alpha(rect, tries=10)
        print color
        print "@"*10
        staged_image = self.ds.stage_draw(rect, color=color)
        diff1 = DrawShape.rmsdiff(self.ds.og_image, staged_image)
        
        print "{d}vs{d1}".format(d=diff1,d1=diff0)
        print "{d}vs{d1}".format(d=diff1,d1=diff)
        self.assertTrue(diff1 < diff0)

    def test_find_best_shape(self):
        diff = DrawShape.rmsdiff(self.ds.og_image, self.ds.image)

        rect = Rect(self.image.size)
        color = average_color(rect, self.ds.og_image)
        staged_image = self.ds.stage_draw(rect, color=color)
        diff0 = DrawShape.rmsdiff(self.ds.og_image, staged_image)

        rect = self.ds.find_best_shape(tries=500)
        color = average_color(rect, self.ds.og_image)
        staged_image = self.ds.stage_draw(rect, color=color)
        diff1 = DrawShape.rmsdiff(self.ds.og_image, staged_image)
        # print "{d}vs{d1}".format(d=diff1,d1=diff0)
        # print "{d}vs{d1}".format(d=diff1,d1=diff)
        # print rect, rect.area()
        self.assertTrue(diff1 < diff0)

    def test_find_best_mutate(self):
        diff = DrawShape.rmsdiff(self.ds.og_image, self.ds.image)

        rect = Rect(self.image.size)
        color = average_color(rect, self.ds.og_image)
        staged_image = self.ds.stage_draw(rect, color=color)
        diff0 = DrawShape.rmsdiff(self.ds.og_image, staged_image)

        # print "base:"
        # print diff0
        rect, color = self.ds.find_best_mutate(rect, tries=10)
        staged_image = self.ds.stage_draw(rect, color=color)
        diff1 = DrawShape.rmsdiff(self.ds.og_image, staged_image)
        # print "{d}vs{d1}".format(d=diff1,d1=diff0)
        # print "{d}vs{d1}".format(d=diff1,d1=diff)
        
        self.assertTrue(diff1 < diff0)


    def test_stage_draw(self):
        rect = Rect(self.image.size)
        color = average_color(rect, self.ds.og_image)
        diff0 = DrawShape.rmsdiff(self.image, self.ds.image)
        staged_image = self.ds.stage_draw(rect, color=color)
        diff1 = DrawShape.rmsdiff(staged_image, self.ds.image)
        self.assertTrue(diff0 != diff1)





if __name__ == '__main__':
    unittest.main()