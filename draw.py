

from PIL import Image, ImageDraw, ImageChops
import math
import random
from drawshape import DrawShape
from rect import Rect
import pdb


ds = DrawShape("pier.JPG")

TOTAL_SHAPES = 50

for i in range(TOTAL_SHAPES):

    rect = Rect(ds.image.size)
    rect, color = ds.find_best(rect, tries=500)
    print rect, rect.area(), color
    ds.draw(rect, color)

    if i%5==0:
        ds.image.show()
        pdb.set_trace()


   

# ds.image.show()


