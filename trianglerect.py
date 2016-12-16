


from PIL import Image, ImageDraw
import numpy as np
# from numpy import random
import random
import matplotlib.pyplot as plt
from skimage.transform import PiecewiseAffineTransform, warp
import scipy
from scipy.misc import toimage
from random import shuffle
import colorsys
from enum import Enum
import util


"""

- triangle
- pie slice
- multiple boxes for grid again
- choosing between triangle and pie slice should measure against "closeness" to og_image.

"""

class Quadrant(Enum):
    top_left = 1
    top_right = 2
    bottom_right = 3
    bottom_left = 4


class TriangleRect():
    def __init__(self, size=(200,200), base_color=(0,0,0), second_color=(0,0,0), n=4, sn=1,
        quadrant=Quadrant.top_left):

        self.width = size[0]
        self.height = size[1]
        self.base_color = base_color
        self.colors = TriangleRect.gen_colors(base_color, n)
        self.colors_secondary = TriangleRect.gen_colors(second_color,sn)
        self.quadrant = quadrant


    @staticmethod
    def __avg_lum(colors):
        cur_lum = 0
        for color in colors:
             cur_lum += util.luminance(color[0], color[1], color[2])

        return round(cur_lum / len(colors), 2)

    def avg_lum(self):
        return TriangleRect.__avg_lum(self.colors)

    @staticmethod
    def gen_colors(base_color, n):
        deg = 30/360.0
        colors = []
        if n==1:
            colors.append(base_color)
        else:   
            # maximum distance between all colors combined
            distance = 40
            colors = []

            r,g,b = base_color
            quad = 1 if util.luminance(r,g,b) > 100 else 0
            # print util.luminance(r,g,b)
            for i in range(-n/2+quad, n/2+quad):
                color = np.asarray(base_color) + (i)*distance/float(n)
                color[0] = util.clamp_int(color[0], 0, 255)
                color[1] = util.clamp_int(color[1], 0, 255)
                color[2] = util.clamp_int(color[2], 0, 255)
                color = tuple(color.astype(int))
                colors.append(color)

        return colors


    @staticmethod
    # def find_best(img):
    def find_best(img, base_color, second_color, n=2, sn=2):
        w,h=img.size
        quads = [Quadrant.top_left, Quadrant.top_right, Quadrant.bottom_left, Quadrant.bottom_right]

        best_trect = None
        best_score = 10000
        for quad in quads:
            trect = TriangleRect(size=(w,h), base_color=base_color, second_color=second_color, n=n, sn=sn,
                quadrant=quad)
            timg = trect.draw()

            score = util.rmsdiff(img, timg)
            if score <= best_score:
                best_trect = trect
                best_score = score

        return best_trect


    # return the perceived hue / luminance for now
    
    def draw(self):
        paper = Image.new('RGBA', (self.width, self.height))
        canvas = ImageDraw.Draw(paper)

        pw = 2#(self.width/len(self.colors))/2

        if random.randrange(2):
            self.colors_secondary = list(reversed(self.colors_secondary))

        if random.randrange(2):
            self.colors = list(reversed(self.colors))

        if len(self.colors)>=3:
            self.colors[1], self.colors[2] = self.colors[2], self.colors[1]

        """
        draw border square
        """
        width = pw
        for idx, color in enumerate(self.colors_secondary):
            paper.paste(color, [width*idx,width*idx, self.width-width*idx, self.height-width*idx])
            # import pdb; pdb.set_trace()


        """
        draw triangles
        """
        x_offset = pw*(len(self.colors_secondary))
        y_offset = pw*(len(self.colors_secondary))
        for idx, color in enumerate(self.colors):
            color = int(color[0]),int(color[1]),int(color[2])
            width,height = self.width-pw*idx, self.height-pw*idx
            sx,sy = (pw*idx),(pw*idx + y_offset)

            if self.quadrant == Quadrant.top_right:
                width-=x_offset
                sx+=x_offset
                coord = [(sx+(idx*pw), sy), (width, sy), (width, height-sy)]
            elif self.quadrant ==  Quadrant.top_left:
                sx+=x_offset
                coord = [(sx, sy), (width-sx, sy), (sx, height-sy)]
            elif self.quadrant ==  Quadrant.bottom_right:
                sx+=x_offset
                width-=x_offset
                height-=y_offset
                coord = [(sx+(idx*pw), height), (width, sy+(idx*pw)), (width, height)]
            elif self.quadrant ==  Quadrant.bottom_left:
                sx+=x_offset
                height-=y_offset
                coord = [(sx, sy+(idx*pw)), (width-sx, height), (sx, height)]

            canvas.polygon(coord, fill=color)

        # paper.show()
        return paper







