

from PIL import Image, ImageDraw, ImageChops
import math
import random
from drawshape import DrawShape
from rect import Rect
from circle import Circle
import pdb

TOTAL_SHAPES = 200

for j in range(1):
    ds = DrawShape("./examples/cat.JPG")
    for i in range(TOTAL_SHAPES):

        rect = ds.find_best_shape(ShapeCls=Circle, tries=50)
        print "best starting rect"
        print rect, rect.area()

        rect = ds.find_best_mutate(rect, tries=100)
        color = ds.find_best_alpha(rect)

        diff0 = DrawShape.rmsdiff(ds.og_image, ds.image)
        staged = ds.stage_draw(rect, color)
        diff1 = DrawShape.rmsdiff(ds.og_image, staged)

        print diff1, diff0
        if diff1 < diff0:
            print "{i} drawing...".format(i=i)
            print rect, rect.area(), color
            ds.draw_shape(rect, color)

        # if i<200:
        #     if i%50 == 0:
        #         ds.image.show()
        if i%50==0:
            ds.image.show()
        #     # import pdb; pdb.set_trace()


    ds.image.show()
    ds.image.save("bloop{j}.JPEG".format(j=j), "JPEG")

