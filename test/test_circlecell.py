

import unittest
from PIL import Image
import util
import numpy as np
from skimage import io, feature
from skimage.color import rgb2grey
from circlecell import CircleCell
from colorpalette import ColorPalette

class TestCircleCell(unittest.TestCase):

    def setUp(self):
        pass
       
    def tearDown(self):
        pass

    def test_find_best(self):
        og_image = Image.open("./examples/test.JPEG")

        # Test lower left jaw
        cropped = og_image.crop((125,370,150,395))

        ccell = CircleCell.find_best(cropped, n=3, sn=2)
        # ccell.draw().show()
        # import pdb; pdb.set_trace()
        # self.assertEqual(trect.quadrant, Quadrant.top_right)

        # Test upper right ear
        crop_right_ear = og_image.crop((340-25,270-25,340+25,270+25))       
        ccell = CircleCell.find_best(crop_right_ear, n=3, sn=3)
        # self.assertEqual(trect.quadrant, Quadrant.bottom_right)

        crop_top_right_ear = og_image.crop((360-25,180-25, 360+25, 180+25))
        ccell = CircleCell.find_best(crop_top_right_ear, n=3, sn=3)
        # self.assertTrue(trect.quadrant == Quadrant.bottom_left or trect.quadrant == Quadrant.top_right)



    def test_draw(self):
        # colors = CircleCell.gen_colors(base_color, n=4)
        ccell = CircleCell(size=(24,12), csize=(24,12), base_color=(100,100,100), 
            second_color=(200,200,200), n=3, sn=2, colorful=False)
        ccell.draw().show()
        ccell = CircleCell(size=(200,200), csize=(200,200), base_color=(100,100,100), 
            second_color=(200,200,200), n=3, sn=2)
        ccell.draw()
        ccell = CircleCell(size=(200,200), csize=(200,200), base_color=(100,100,100), 
            second_color=(200,200,200), n=3, sn=2)
        ccell.draw()
        ccell = CircleCell(size=(200,200), csize=(200,200), base_color=(100,100,100), 
            second_color=(200,200,200), n=3, sn=2)
        ccell.draw()


if __name__ == '__main__':
    unittest.main()