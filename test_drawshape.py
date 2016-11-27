
import unittest
from drawshape import DrawShape
from PIL import Image

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

    def test_random_pos(self):
        x,y = self.ds.random_pos()
        w,h = self.ds.image.size
        self.assertTrue(x > 0 and x <= w)
        self.assertTrue(y > 0 and y <= h)


    def test_random_rects(self):
        tries = 10
        rects = self.ds.random_rects(pos=(100,100), max_size=500, tries=10)
        self.assertTrue(len(rects) == 10)

    def test_area_rect(self):
        p0 = (0,0)
        p1 = (100,100)
        rect = [p0,p1]
        area = self.ds.rect_area(rect)
        self.assertEqual(area, 10000)

        p0 = (-50, -50)
        p1 = (50, 50)
        rect = [p0, p1]
        area = self.ds.rect_area(rect)
        self.assertEqual(area, 10000)

        p0 = (-100, 0)
        p1 = (0, 100)
        rect = [p0, p1]
        area = self.ds.rect_area(rect)
        self.assertEqual(area, 10000)

    def test_stage_draw(self):
        pos = (100,100)
        r,g,b = self.ds.og_image.getpixel(pos)

        diff0 = DrawShape.rmsdiff(self.image, self.ds.image)
        rect = self.ds.random_rects(pos=pos, max_size=500)
        staged_image = self.ds.stage_draw(rect[0], color=(r,g,b))
        diff1 = DrawShape.rmsdiff(staged_image, self.ds.image)
        self.assertTrue(diff0 != diff1)


    def test_commit_draw(self):
        # Generate small rects to minimize rms
        pos = (100,100)
        rects = self.ds.random_rects(pos=pos, max_size=5, tries=1)
        color = self.ds.og_image.getpixel(pos)

        staged_image = self.ds.stage_draw(rects[0], color=color)
        diff0 = DrawShape.rmsdiff(staged_image, self.image)
        diff1 = DrawShape.rmsdiff(self.ds.image, self.image)
        if (diff0 < diff1):
            self.ds.commit_draw(staged_image)

        diff2 = DrawShape.rmsdiff(self.ds.image , self.image)
        self.assertTrue(diff2 < diff1)
        self.assertTrue(diff0 == diff2)
        




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