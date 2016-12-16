

import unittest
from PIL import Image
import util
import numpy as np
from skimage import io, feature
from skimage.color import rgb2grey
from trianglerect import TriangleRect
from trianglerect import Quadrant
from colorpalette import ColorPalette

class TestCompColor(unittest.TestCase):

    def setUp(self):
        pass
       
    def tearDown(self):
        pass

    def test_avg_lum(self):
        triangle = TriangleRect(size=(200,200), base_color=(100,100,100), 
            second_color=(200,200,200), n=4, sn=1, quadrant=Quadrant.top_right)
        self.assertEqual(triangle.avg_lum(), 95)

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

    def test_find_best(self):
        og_image = Image.open("./examples/test.JPEG")
        cropped = og_image.crop((125,370,150,395))
        cropped_array = np.array(cropped)

        img_edges = feature.canny(rgb2grey(cropped_array), sigma=3)

        # quantized_array = ColorPalette.quantize_pil_image(cropped, 2)
        fg,bg = ColorPalette.average_colors(cropped,2)
        
        import pdb; pdb.set_trace()

        # def edge_colors(img_edges):

        x_line,y_line = np.where(img_edges==True)
        prim_color = util.average_color_pixels(cropped, zip(x_line, y_line))
        x_bg,y_bg = np.where(img_edges==False)
        bg_color = util.average_color_pixels(cropped, zip(x_bg,y_bg))



        trect = TriangleRect.find_best(cropped, bg_color, prim_color, n=2, sn=2)
        import pdb; pdb.set_trace()
        self.assertTrue(trect.quadrant, Quadrant.top_right)


    def test_draw(self):
        # colors = TriangleRect.gen_colors(base_color, n=4)
        triangle = TriangleRect(size=(200,200), base_color=(100,100,100), 
            second_color=(200,200,200), n=3, sn=2, quadrant=Quadrant.bottom_right)
        triangle.draw()
        triangle = TriangleRect(size=(200,200), base_color=(100,100,100), 
            second_color=(200,200,200), n=3, sn=2, quadrant=Quadrant.bottom_left)
        triangle.draw()
        triangle = TriangleRect(size=(200,200), base_color=(100,100,100), 
            second_color=(200,200,200), n=3, sn=2, quadrant=Quadrant.top_left)
        triangle.draw()
        triangle = TriangleRect(size=(200,200), base_color=(100,100,100), 
            second_color=(200,200,200), n=3, sn=2, quadrant=Quadrant.top_right)
        triangle.draw()


if __name__ == '__main__':
    unittest.main()