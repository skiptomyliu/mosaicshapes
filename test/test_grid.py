

import unittest
from grid import Grid


class TestGrid(unittest.TestCase):

    def setUp(self):
        self.grid = Grid("./examples/bill.JPEG")
        pass
       
    def tearDown(self):
        pass

    # Test vertical expansion
    def test_warp(self):
        self.grid.warp()


    def test_occupy(self):
        x,y = (10,20)
        self.grid.occupy(x,y)
        result = self.grid.is_occupied(x,y)
        self.assertTrue(result)

    # Test vertical expansion
    def test_is_occupied(self):
        x,y = (10,20)
        result = self.grid.is_occupied(x,y)
        self.assertFalse(result)
        self.grid.occupy(x,y)
        result = self.grid.is_occupied(x,y)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()