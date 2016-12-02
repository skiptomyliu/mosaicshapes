
from shape import Shape
from rect import Rect
import random
from util import *

class Circle(Rect):
    def __init__(self, bound_size, coords=None):
        self.bound_size = bound_size

        if not coords:
            self.random()
        else:
            self.x0 = coords[0]
            self.y0 = coords[1]
            self.x1 = coords[2]
            self.y1 = coords[3]

    def draw(self, canvas, color):
        print "circle"
        canvas.ellipse(self.coords(), fill=color)

    def __str__(self):
        return "({x},{y}),({x1},{y1})".format(x=self.x0, y=self.y0, x1=self.x1, y1=self.y1)

