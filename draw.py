

from PIL import Image, ImageDraw, ImageChops
import math
import random
from drawshape import DrawShape
import pdb


ds = DrawShape("pier.JPG")

t = 300
for i in range(0,t):
    print i
    for j in range(0,i):
        w,h = t-i,t-i
            
        if bool(random.getrandbits(1)):
            # ds.draw_circle((w,h))    
            ds.draw_circle((w,h))    
            # ds.draw_rect((w,h))
        else:
            # ds.draw_circle((w,h))    
            ds.draw_rect((w,h))

# for i in range(0, 10000):
#     ds.draw_rect_rand_size()

ds.image.show()