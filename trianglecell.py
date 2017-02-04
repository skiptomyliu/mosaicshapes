


from PIL import Image, ImageDraw
import numpy as np
from colorpalette import ColorPalette
import random
from skimage.transform import PiecewiseAffineTransform, warp
import scipy
from scipy.misc import toimage
from random import shuffle
import util
from cell import Cell, Quadrant

"""

- triangle
- pie slice
- multiple boxes for grid again
- choosing between triangle and pie slice should measure against "closeness" to og_image.

"""

class TriangleCell(Cell):
    def __init__(self, size=(200,200), base_color=(0,0,0), second_color=(0,0,0), 
        shrink=0, n=4, sn=1, quadrant=Quadrant.top_left, colorful=True):

        self.width = size[0]
        self.height = size[1]
        self.base_color = base_color

        self.colors = Cell.gen_colors(base_color, n, colorful)
        self.colors_secondary = Cell.gen_colors(second_color,sn, colorful)
        self.quadrant = quadrant
        self.shrink = shrink

    @staticmethod
    def __avg_lum(colors):
        cur_lum = 0
        for color in colors:
             cur_lum += util.luminance(color[0], color[1], color[2])

        return round(cur_lum / len(colors), 2)

    def avg_lum(self):
        return TriangleCell.__avg_lum(self.colors)


    @staticmethod
    def find_best(img, n=2, sn=2, base_color=(0,0,0), second_color=(0,0,0), colorful=True):
        color_combos = [[second_color,base_color], [base_color, second_color]]
        quads = [Quadrant.top_left, Quadrant.top_right, Quadrant.bottom_left, Quadrant.bottom_right]

        w,h=img.size
        best_trect = None
        best_score = 10000
        for quad in quads:
            for color_combo in color_combos:
                trect = TriangleCell(size=(w,h), 
                    base_color=color_combo[0], second_color=color_combo[1], 
                    shrink=0, n=n, sn=sn, quadrant=quad, colorful=colorful)

                timg = trect.draw()
                score = util.rmsdiff(img, timg)
                if score <= best_score:
                    best_trect = trect
                    best_score = score

        return best_trect

    # return the perceived hue / luminance for now
    def draw(self):

        N=2
        # pw = 4 #(self.width/len(self.colors))/2
        shortest = self.width if self.width < self.height else self.height
        pw = int(round(.5 * .5 * shortest * 1/(len(self.colors) + len(self.colors_secondary))))



        # pw = 30
        # pw = 10
        # print pw
        paper = Image.new('RGBA', (self.width*N, self.height*N))
        canvas = ImageDraw.Draw(paper, paper.mode)

        # if random.randrange(2):
            # self.colors_secondary = list(reversed(self.colors_secondary))

        if len(self.colors)>=3:
            self.colors[1], self.colors[2] = self.colors[2], self.colors[1]

        """
        draw border square
        """
        width = pw
        for idx, color in enumerate(self.colors_secondary):
            paper.paste(color, [width*idx*N, width*idx*N, (self.width-width*idx)*N, (self.height-width*idx)*N])

        """
        draw triangles
        """

        x_offset = pw*(len(self.colors_secondary))+self.shrink
        y_offset = pw*(len(self.colors_secondary))+self.shrink
        for idx, color in enumerate(self.colors):
            color = int(color[0]),int(color[1]),int(color[2])
            width,height = self.width-pw*idx, self.height-pw*idx
            sx,sy = (pw*idx*pw), (pw*idx + y_offset)

            sx = int(round(len(self.colors)*pw/2.0))
            sx += (pw*idx)
            ex = self.width - sx

            coord = [((sx + pw*idx*(self.width/float(self.height))*1.5)*N, sy*N), (ex*N, sy*N), (ex*N, (height-sy-idx*pw*(self.height/self.width))*N)]

            canvas.polygon(coord, fill=color)
        # import pdb; pdb.set_trace()

        if self.quadrant == Quadrant.top_right:
            pass
        elif self.quadrant ==  Quadrant.top_left:
            paper = paper.rotate(90)
        elif self.quadrant ==  Quadrant.bottom_right:
            paper = paper.rotate(-90)
        elif self.quadrant ==  Quadrant.bottom_left:
            paper = paper.rotate(180)
        
        # import pdb; pdb.set_trace()
        del canvas
        paper.thumbnail((self.width, self.height)) 

        return paper







