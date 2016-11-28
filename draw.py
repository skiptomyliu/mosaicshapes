

from PIL import Image, ImageDraw, ImageChops
import math
import random
from drawshape import DrawShape
from rect import Rect
import pdb


ds = DrawShape("pier.JPG")

TOTAL_SHAPES = 200

for i in range(TOTAL_SHAPES):

    rect = ds.find_best_shape(tries=500)
    print "best starting rect"
    print rect, rect.area()

    rect, color = ds.find_best_mutate(rect, tries=100)
    color = ds.find_best_alpha(rect)
    # print color

    diff0 = DrawShape.rmsdiff(ds.og_image, ds.image)

    staged = ds.stage_draw(rect, color)
    diff1 = DrawShape.rmsdiff(ds.og_image, staged)

    print diff1, diff0
    if diff1 < diff0:
        print "drawing..."
        print rect, rect.area(), color
        ds.draw_shape(rect, color)


    if i%25==0:
        ds.image.show()
        # import pdb; pdb.set_trace()
        


   

ds.image.show()


