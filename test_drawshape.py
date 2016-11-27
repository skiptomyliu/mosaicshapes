
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


    def test_draw_rect(self):
        size = (100, 100)
        diff1 = DrawShape.rmsdiff(self.image, self.ds.image)
        self.ds.draw_rect(size)
        diff2 = DrawShape.rmsdiff(self.image, self.ds.image)
        self.assertTrue(diff2 < diff1)

    def test_draw_rect_rand_size(self):
        diff1 = DrawShape.rmsdiff(self.image, self.ds.image)
        self.ds.draw_rect_rand_size()
        diff2 = DrawShape.rmsdiff(self.image, self.ds.image)
        self.assertTrue(diff2 < diff1)


    # def test_decay(self):
    #     size = (100, 100)





if __name__ == '__main__':
    unittest.main()