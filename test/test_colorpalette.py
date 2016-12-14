
import unittest
from colorpalette import ColorPalette
from sklearn.datasets import load_sample_image
from skimage import io

class TestColorPalette(unittest.TestCase):

    def setUp(self):
        self.pal = ColorPalette()
        self.pal.quantize("./examples/bill.JPEG", 64)
        pass
       
    def tearDown(self):
        pass

    def test_translate_color(self):
    	r,g,b = (100,0,0)
    	self.pal.translate_color(color=(r,g,b))

    def test_apply_palette_to_image(self):
    	# china = load_sample_image("china.jpg")
    	self.pal.quantize("./examples/bill.JPEG", 12)
    	# self.pal.apply_palette_to_image(china)
    	self.pal.apply_palette_to_image(io.imread("./examples/bill.JPEG"))

    # def test_quantize(self):



if __name__ == '__main__':
    unittest.main()