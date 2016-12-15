

import unittest
from trianglerect import TriangleRect
from trianglerect import Quadrant

class TestCompColor(unittest.TestCase):

    def setUp(self):
        pass
       
    def tearDown(self):
        pass

    def test_avg_lum(self):
        triangle = TriangleRect(size=(200,200))
        triangle.colors.append((0,0,0))
        triangle.colors.append((255,255,255))
        self.assertEqual(triangle.avg_lum(), 127.5)

    # def test_gen_colors(self):
    #     base_color = (200,200,200)
    #     colors = CompColor.gen_colors(base_color, n=1)
    #     self.assertEqual(len(colors), 1)
    #     self.assertEqual(colors[0], base_color)

    #     colors = CompColor.gen_colors(base_color, n=2)
    #     self.assertEqual(len(colors), 2)
    #     self.assertEqual(colors, [(200.0, 200.0, 200.0), (220.0, 220.0, 220.0)])

    #     base_color = (245,245,245)
    #     colors = CompColor.gen_colors(base_color, n=2)
    #     self.assertEqual(len(colors), 2)
    #     self.assertEqual(colors, [(245.0, 245.0, 245.0), (255.0, 255.0, 255.0)])

    #     base_color = (200,200,200)
    #     colors = CompColor.gen_colors(base_color, n=3)
    #     self.assertEqual(len(colors), 3)
    #     self.assertEqual(colors, [(186.0, 186.0, 186.0), (200.0, 200.0, 200.0), (213.0, 213.0, 213.0)])

    #     base_color = (100,100,100)
    #     colors = CompColor.gen_colors(base_color, n=4)
    #     self.assertEqual(len(colors), 4)
    #     self.assertEqual(colors, [(80.0, 80.0, 80.0), (90.0, 90.0, 90.0), (100.0, 100.0, 100.0), (110.0, 110.0, 110.0)])

    def test_draw(self):
        base_color = (100,100,100)
        colors = TriangleRect.gen_colors(base_color, n=4)
        triangle = TriangleRect(size=(200,200), base_color=(200,200,200), quadrant=Quadrant.top_right)
        triangle.colors = colors
        triangle.draw()


if __name__ == '__main__':
    unittest.main()