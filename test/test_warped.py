

import unittest
from warped import Warped

class TestWarped(unittest.TestCase):

    def setUp(self):
        pass
       
    def tearDown(self):
        pass

    def test_width(self):
        warped = Warped(size=(200,200), color=(180,0,200))
        self.assertEqual(200, warped.width)

    def test_height(self):
        warped = Warped(size=(200,200), color=(180,0,200))
        self.assertEqual(200, warped.height)

    # def test_draw(self):
    #     warped = Warped(size=(200,200), color=(180,0,200))
    #     warped.draw()

    # # Test horizontal expansion
    # def test_draw(self):
    #     warped = Warped(size=(50,20), color=(180,0,200))
    #     warped.draw()

    # Test vertical expansion
    def test_draw(self):
        # warped = Warped(size=(200,100), color=(180,0,200))
        # warped.draw()

        # warped = Warped(size=(50,20), color=(180,0,200))
        # warped.draw()

        warped = Warped(size=(200,200), color=(180,0,200))
        warped.draw()

    def test_draw_angle(self):
        # warped = Warped(size=(200,100), color=(180,0,200))
        # warped.draw()

        # warped = Warped(size=(50,20), color=(180,0,200))
        # warped.draw()

        warped = Warped(size=(200,200), color=(180,0,200), )
        warped.draw()


if __name__ == '__main__':
    unittest.main()