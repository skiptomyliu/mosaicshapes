
from shape import Shape
from rect import Rect
import random
from util import *

class Circle(Rect):
    def draw(self, canvas, color):
        print "circle"
        canvas.ellipse(self.coords(), fill=color)

    def __str__(self):
        return "({x},{y}),({x1},{y1})".format(x=self.x0, y=self.y0, x1=self.x1, y1=self.y1)