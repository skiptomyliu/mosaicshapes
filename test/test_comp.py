

import unittest
from comp import CompColor


class TestCompColor(unittest.TestCase):

    def setUp(self):
        pass
       
    def tearDown(self):
        pass

    def test_avg_lum(self):
        ccolor = CompColor(size=(200,200))
        ccolor.colors.append((0,0,0))
        ccolor.colors.append((255,255,255))
        self.assertEqual(ccolor.avg_lum(ccolor.colors), 127.5)




if __name__ == '__main__':
    unittest.main()