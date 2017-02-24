

import unittest
from PIL import Image
import util
import numpy as np
from skimage import io, feature
from pieslicecell import PieSliceCell
from cell import Quadrant
from colorpalette import ColorPalette

class TestPieSliceCell(unittest.TestCase):

    def setUp(self):
        pass
       
    def tearDown(self):
        pass


    def test_find_best(self):
        og_image = Image.open("./examples/test.JPEG")

        # Test lower left jaw
        cropped = og_image.crop((125,370,150,395))
        trect = PieSliceCell.find_best(cropped, n=3, sn=2)
        # cropped.show()
        # trect.draw().show()
        # import pdb; pdb.set_trace()
        # self.assertEqual(trect.quadrant, Quadrant.top_right)


        # Test upper right ear
        crop_right_ear = og_image.crop((340-25,270-25,340+25,270+25))       
        trect = PieSliceCell.find_best(crop_right_ear, n=2, sn=3)
        # crop_right_ear.show()
        # trect.draw().show()
        # self.assertEqual(trect.quadrant, Quadrant.bottom_right)
        
        # # test upper left ear
        # crop_left_ear = og_image.crop((50-25,200-25, 50+25, 200+25))
        # # trect = PieSliceCell.find_best(crop_left_ear, n=2, sn=3)
        # # print trect.quadrant
        # # import pdb; pdb.set_trace()
        # # self.assertTrue(trect.quadrant == Quadrant.bottom_right or trect.quadrant == Quadrant.top_left)

        # crop_top_right_ear = og_image.crop((360-25,180-25, 360+25, 180+25))
        # trect = PieSliceCell.find_best(crop_top_right_ear, n=2, sn=3)
        # self.assertTrue(trect.quadrant == Quadrant.bottom_left or trect.quadrant == Quadrant.top_right)


    def test_draw(self):
        pcell = PieSliceCell(size=(100,100), base_color=(100,100,100), 
            second_color=(200,200,200), n=3, sn=2, quadrant=Quadrant.bottom_right, colorful=False)
        pcell.draw().show()

        pcell = PieSliceCell(size=(20,20), base_color=(100,100,100), 
            second_color=(200,200,200), n=3, sn=3, quadrant=Quadrant.bottom_right, colorful=False)
        pcell.draw().show()

        pcell = PieSliceCell(size=(200,200), base_color=(100,100,100), 
            second_color=(200,200,200), n=3, sn=2, quadrant=Quadrant.bottom_right)
        pcell.draw()
        pcell = PieSliceCell(size=(200,200), base_color=(100,100,100), 
            second_color=(200,200,200), n=3, sn=2, quadrant=Quadrant.bottom_left)
        pcell.draw()
        pcell = PieSliceCell(size=(200,200), base_color=(100,100,100), 
            second_color=(200,200,200), n=3, sn=2, quadrant=Quadrant.top_left)
        pcell.draw()
        pcell = PieSliceCell(size=(200,200), base_color=(100,100,100), 
            second_color=(200,200,200), n=3, sn=2, quadrant=Quadrant.top_right)
        pcell.draw()


if __name__ == '__main__':
    unittest.main()