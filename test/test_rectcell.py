

import unittest
from PIL import Image
import util
import numpy as np
from skimage import io, feature
from skimage.color import rgb2grey
from rectcell import RectCell
from colorpalette import ColorPalette

class TestRectCell(unittest.TestCase):

    def setUp(self):
        pass
       
    def tearDown(self):
        pass

    def test_find_best(self):
        og_image = Image.open("./examples/test.JPEG")

        # Test lower left jaw
        cropped = og_image.crop((330-23,290,330,290+50))
        # cropped.show()
        fg,bg = ColorPalette.quantize_img(cropped, 2)
        csize_w, csize_h = cropped.size[0]-9,cropped.size[1]-9
        trect = RectCell(size=cropped.size, csize=(csize_w, csize_h), base_color=bg, second_color=fg, n=4, sn=1)

        # self.assertEqual(trect.quadrant, Quadrant.top_right)
        # Test upper right ear
        crop_right_ear = og_image.crop((340-25,270-25,340+50,270+25))       
        trect = RectCell.find_best(crop_right_ear, n=3, sn=2)
        # crop_right_ear.show()
        # trect.draw().show()

        crop_top_right_ear = og_image.crop((360-25,180-25, 360+25, 180+25))
        trect = RectCell.find_best(crop_top_right_ear, n=3, sn=3)
        # self.assertTrue(trect.quadrant == Quadrant.bottom_left or trect.quadrant == Quadrant.top_right)



    def test_draw(self):
        ccell = RectCell(size=(200,100), csize=(100,100), base_color=(100,100,100), 
            second_color=(200,200,200), n=2, sn=1, colorful=False)
        ccell.draw().show()
        ccell = RectCell(size=(200,200), csize=(200,200), base_color=(100,100,100), 
            second_color=(200,200,200), n=3, sn=2)
        ccell.draw()
        ccell = RectCell(size=(200,200), csize=(200,200), base_color=(100,100,100), 
            second_color=(200,200,200), n=3, sn=2)
        ccell.draw()
        ccell = RectCell(size=(200,200), csize=(200,200), base_color=(100,100,100), 
            second_color=(200,200,200), n=3, sn=2)
        ccell.draw()


if __name__ == '__main__':
    unittest.main()