

import unittest
from PIL import Image
import util
import numpy as np
from skimage import io, feature
from halfcirclecell import HalfCircleCell
from cell import Direction
from colorpalette import ColorPalette

class TestHalfCircleCell(unittest.TestCase):

    def setUp(self):
        pass
       
    def tearDown(self):
        pass

    def test_draw(self):

        pcell = HalfCircleCell(size=(10,10), base_color=(100,100,100), 
            second_color=(200,200,200), n=3, sn=2, direction=Direction.top, colorful=False)
        pcell.draw().show()

        pcell = HalfCircleCell(size=(500,500), base_color=(100,100,100), 
            second_color=(200,200,200), n=3, sn=2, direction=Direction.top, colorful=False)
        pcell.draw()
        pcell = HalfCircleCell(size=(200,200), base_color=(100,100,100), 
            second_color=(200,200,200), n=3, sn=2, direction=Direction.right)
        pcell.draw()
        pcell = HalfCircleCell(size=(200,200), base_color=(100,100,100), 
            second_color=(200,200,200), n=3, sn=2, direction=Direction.bottom)
        pcell.draw()
        pcell = HalfCircleCell(size=(200,200), base_color=(100,100,100), 
            second_color=(200,200,200), n=3, sn=2, direction=Direction.left)
        pcell.draw()

if __name__ == '__main__':
    unittest.main()