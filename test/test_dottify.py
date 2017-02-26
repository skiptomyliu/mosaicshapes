



import unittest
from PIL import Image
import util
from dottify import Dottify

class TestDottify(unittest.TestCase):

    def setUp(self):
        self.dottify = Dottify("/Users/dean/Desktop/bo.jpg")
        pass
       
    def tearDown(self):
        pass

    def test_paint(self):
        self.dottify.paint()



if __name__ == '__main__':
    unittest.main()