

import unittest
from drawwarped import DrawWarped


class TestDrawWarped(unittest.TestCase):

    def setUp(self):
        self.dw = DrawWarped("./examples/bill.JPEG")
        pass
       
    def tearDown(self):
        pass

    # Test vertical expansion
    def test_warp(self):
        self.dw.warp()

    def test_occupy(self):
        x,y = (10,20)
        self.dw.occupy(x,y)
        result = self.dw.is_occupied(x,y)
        self.assertTrue(result)

    # Test vertical expansion
    def test_is_occupied(self):
        x,y = (10,20)
        result = self.dw.is_occupied(x,y)
        self.assertFalse(result)
        self.dw.occupy(x,y)
        result = self.dw.is_occupied(x,y)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()