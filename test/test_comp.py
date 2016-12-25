

import unittest
from comp import CompColor


class TestCompColor(unittest.TestCase):

    def setUp(self):
        pass
       
    def tearDown(self):
        pass

    def test_avg_lum(self):
        ccolor = CompColor(size=(200,200))
        ccolor.colors.append((0,0,0))
        ccolor.colors.append((255,255,255))
        # self.assertEqual(ccolor.avg_lum(ccolor.colors), 127.5)

    def test_gen_colors(self):
        base_color = (200,200,200)
        colors = CompColor.gen_colors(base_color, n=1)
        self.assertEqual(len(colors), 1)
        self.assertEqual(colors[0], base_color)

        colors = CompColor.gen_colors(base_color, n=2)
        self.assertEqual(len(colors), 2)
        self.assertEqual(colors, [(200.0, 200.0, 200.0), (220.0, 220.0, 220.0)])

        base_color = (245,245,245)
        colors = CompColor.gen_colors(base_color, n=2)
        self.assertEqual(len(colors), 2)
        self.assertEqual(colors, [(245.0, 245.0, 245.0), (255.0, 255.0, 255.0)])

        base_color = (200,200,200)
        colors = CompColor.gen_colors(base_color, n=3)
        self.assertEqual(len(colors), 3)
        self.assertEqual(colors, [(186.0, 186.0, 186.0), (200.0, 200.0, 200.0), (213.0, 213.0, 213.0)])

        base_color = (100,100,100)
        colors = CompColor.gen_colors(base_color, n=4)
        self.assertEqual(len(colors), 4)
        self.assertEqual(colors, [(80.0, 80.0, 80.0), (90.0, 90.0, 90.0), (100.0, 100.0, 100.0), (110.0, 110.0, 110.0)])

        # base_color = (5,5,5)
        # colors = CompColor.gen_colors(base_color, n=4)
        # self.assertEqual(len(colors), 4)
        # self.assertEqual(colors, [(90.0, 90.0, 90.0), (100.0, 100.0, 100.0), (110.0, 110.0, 110.0), (120.0, 120.0, 120.0)])

    def test_draw_circle(self):
        ccolor = CompColor(size=(25, 25), base_color=[180,180,180], n=3)
        img = ccolor.draw_circle()
        # img.show()

    def test_draw(self):
        base_color = (100,100,100)
        colors = CompColor.gen_colors(base_color, n=4)
        ccolor = CompColor(size=(200,200))
        ccolor.colors = colors
        ccolor.draw()


if __name__ == '__main__':
    unittest.main()