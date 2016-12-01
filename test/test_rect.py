
import unittest

from rect import Rect

class TestRect(unittest.TestCase):

    def setUp(self):
        self.w,self.h = (500,500)
        self.rect = Rect(bound_size=(self.w, self.h))

    def tearDown(self):
        pass

    def test_init_random(self):
        rect = Rect.init_random(bound_size=(self.w, self.h))
        print rect
        pass

    def test_init_coords(self):
        coords = [0,0,100,100]
        rect = Rect.init_coords(bound_size=(self.w, self.h), coords=coords)
        self.assertTrue(rect.x0 == 0 and rect.y0 == 0 and rect.x1 == 100 and rect.y1 == 100)

    def test_coords(self):
        self.assertEqual(self.rect.coords(), 
            [self.rect.x0, self.rect.y0, self.rect.x1, self.rect.y1])

    def test_random(self):
        self.assertTrue(self.rect.x0 > 0 and self.rect.x0 <= self.w)
        self.assertTrue(self.rect.y0 > 0 and self.rect.y0 <= self.h)

        self.assertTrue(abs(self.rect.x0-self.rect.x1) <= self.w)
        self.assertTrue(abs(self.rect.y0-self.rect.y1) <= self.h)

    def test_mutate(self):
        self.rect.mutate()
        self.assertTrue(self.rect.x0 > 0 and self.rect.x0 <= self.w)
        self.assertTrue(self.rect.y0 > 0 and self.rect.y0 <= self.h)

        self.assertTrue(abs(self.rect.x0-self.rect.x1) <= self.w)
        self.assertTrue(abs(self.rect.y0-self.rect.y1) <= self.h)


    def test_area_rect(self):

        pass

        # p0 = (0,0)
        # p1 = (100,100)
        # rect = [p0,p1]
        # area = self.ds.rect_area(rect)
        # self.assertEqual(area, 10000)

        # p0 = (-50, -50)
        # p1 = (50, 50)
        # rect = [p0, p1]
        # area = self.ds.rect_area(rect)
        # self.assertEqual(area, 10000)

        # p0 = (-100, 0)
        # p1 = (0, 100)
        # rect = [p0, p1]
        # area = self.ds.rect_area(rect)
        # self.assertEqual(area, 10000)


if __name__ == '__main__':
    unittest.main()