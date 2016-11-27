

from PIL import Image, ImageDraw, ImageChops
import math
import random
from drawshape import DrawShape
import pdb


ds = DrawShape("pier.JPG")

# t = 300
# for i in range(0,t):
#     print i
#     for j in range(0,i):
#         w,h = t-i,t-i
            
#         if bool(random.getrandbits(1)):
#             # ds.draw_circle((w,h))    
#             ds.draw_circle((w,h))    
#             # ds.draw_rect((w,h))
#         else:
#             # ds.draw_circle((w,h))    
#             ds.draw_rect((w,h))


MAX_SIZE = 1000
MIN_SIZE = 2
TOTAL_SHAPES = 2000

smallest_rect = 10000

# divide by 2
DECAY_RATE = 2
NOT_FOUND = 1 # in a row before decay

cur_not_found = 0
for i in range(TOTAL_SHAPES):
    if i%500 == 0:
        print "MAX_SIZE"
        print MAX_SIZE
        # import pdb; pdb.set_trace()

    pos = ds.random_pos()
    rects = ds.random_rects(pos, MAX_SIZE, tries=10)

    color = ds.og_image.getpixel(pos)
        
    for idx, rect in enumerate(rects):
        cur = DrawShape.rect_area(rect)
        if cur < smallest_rect:
            smallest_rect = cur

            print smallest_rect

        staged_image = ds.stage_draw(rect, color)
        diff0 = DrawShape.rmsdiff(ds.og_image, ds.image)
        diff1 = DrawShape.rmsdiff(ds.og_image, staged_image)

        if diff1 < diff0 and diff1:
            ds.commit_draw(staged_image)
            cur_not_found = 0
            print diff1, diff0
            continue

        if idx == len(rects)-1:
            cur_not_found += 1
            if cur_not_found > NOT_FOUND:
                cur_not_found = 0
                MAX_SIZE = max(MAX_SIZE / DECAY_RATE, 10)


            print "NOTHING FOUND IN CUR BATCH {r}".format(r=cur_not_found)

ds.image.show()


