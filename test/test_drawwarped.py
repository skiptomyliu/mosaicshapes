

import unittest
from drawwarped import DrawWarped

class TestDrawWarped(unittest.TestCase):

    def setUp(self):
        pass
       
    def tearDown(self):
        pass

    # Test vertical expansion
    def test_warp(self):
        dw = DrawWarped("./examples/bill.JPEG")
        dw.warp()


if __name__ == '__main__':
    unittest.main()