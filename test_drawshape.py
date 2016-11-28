
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


    def test_find_best(self):
        diff = DrawShape.rmsdiff(self.ds.og_image, self.ds.image)

        rect = Rect(self.image.size)
        color = average_color(rect, self.ds.og_image)
        staged_image = self.ds.stage_draw(rect, color=color)
        diff0 = DrawShape.rmsdiff(self.ds.og_image, staged_image)

        # print "base:"
        # print diff0
        rect, color = self.ds.find_best(rect, tries=500)
        staged_image = self.ds.stage_draw(rect, color=color)
        diff1 = DrawShape.rmsdiff(self.ds.og_image, staged_image)
        print "{d}vs{d1}".format(d=diff1,d1=diff0)
        print "{d}vs{d1}".format(d=diff1,d1=diff)
        
        self.assertTrue(diff1 < diff0)


    def test_stage_draw(self):
        rect = Rect(self.image.size)
        color = average_color(rect, self.ds.og_image)
        diff0 = DrawShape.rmsdiff(self.image, self.ds.image)
        staged_image = self.ds.stage_draw(rect, color=color)
        diff1 = DrawShape.rmsdiff(staged_image, self.ds.image)
        self.assertTrue(diff0 != diff1)


    # def test_commit_draw(self):
    #     rect = Rect(self.image.size)
    #     color = average_color(rect, self.ds.og_image)

    #     staged_image = self.ds.stage_draw(rect, color=color)
    #     diff0 = DrawShape.rmsdiff(staged_image, self.image)
    #     diff1 = DrawShape.rmsdiff(self.ds.image, self.image)
    #     if (diff0 < diff1):
    #         self.ds.commit_draw(staged_image)

    #     diff2 = DrawShape.rmsdiff(self.ds.image , self.image)
    #     self.assertTrue(diff2 < diff1)
    #     self.assertTrue(diff0 == diff2)
        




    # def test_draw_rect(self):
    #     size = (100, 100)
    #     diff1 = DrawShape.rmsdiff(self.image, self.ds.image)
    #     self.ds.draw_rect(size)
    #     diff2 = DrawShape.rmsdiff(self.image, self.ds.image)
    #     self.assertTrue(diff2 < diff1)

    # def test_draw_rect_rand_size(self):
    #     diff1 = DrawShape.rmsdiff(self.image, self.ds.image)
    #     self.ds.draw_rect_rand_size()
    #     diff2 = DrawShape.rmsdiff(self.image, self.ds.image)
    #     self.assertTrue(diff2 < diff1)


    def stage_draw(self):
        pass

    def commit_draw(self):
        pass
    # def test_decay(self):
    #     size = (100, 100)





if __name__ == '__main__':
    unittest.main()