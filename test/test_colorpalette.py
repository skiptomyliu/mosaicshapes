
import unittest
from colorpalette import ColorPalette


class TestColorPalette(unittest.TestCase):

    def setUp(self):
        self.pal = ColorPalette()
        self.pal.quantize("./examples/bill.JPEG")
        pass
       
    def tearDown(self):
        pass

    def test_translate_color(self):
    	r,g,b = (100,0,0)
    	
    	self.pal.translate_color(color=(r,g,b))
    	pass


if __name__ == '__main__':
    unittest.main()