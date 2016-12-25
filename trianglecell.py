


from PIL import Image, ImageDraw
import numpy as np
from colorpalette import ColorPalette
import random
import matplotlib.pyplot as plt
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
        shrink=0, n=4, sn=1, quadrant=Quadrant.top_left):

        self.width = size[0]
        self.height = size[1]
        self.base_color = base_color

        self.colors = Cell.gen_colors(base_color, n)
        self.colors_secondary = Cell.gen_colors(second_color,sn)
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


    # Should we use this??
    @staticmethod
    def find_best_xy(draw_img, cropped_img, (x,y), n=2, sn=1):
        fg,bg = ColorPalette.average_colors(cropped_img,2)
        second_color = (fg*255).astype(int)
        base_color = (bg*255).astype(int)

        quads = [Quadrant.top_left, Quadrant.top_right, Quadrant.bottom_left, Quadrant.bottom_right]

        w,h=cropped_img.size
        best_trect = None
        best_score = 10000
        for quad in quads:
            trect = TriangleCell(size=(w,h), base_color=base_color, second_color=second_color, 
                shrink=0, n=n, sn=sn, quadrant=quad)

            timg = trect.draw()
            staged_image = draw_img.copy()
            staged_image.paste(timg, (x,y))           

            score = util.rmsdiff(draw_img, staged_image)
            print quad, score
            if score <= best_score:
                best_trect = trect
                best_score = score

        return best_trect

    @staticmethod
    def find_best(img, n=2, sn=2):
        second_color,base_color = ColorPalette.quantize_img(img,2)
        
        color_combos = [[second_color,base_color], [base_color, second_color]]

        quads = [Quadrant.top_left, Quadrant.top_right, Quadrant.bottom_left, Quadrant.bottom_right]

        w,h=img.size
        best_trect = None
        best_score = 10000
        for quad in quads:
            for color_combo in color_combos:
                trect = TriangleCell(size=(w,h), 
                    base_color=color_combo[0], second_color=color_combo[1], 
                    shrink=0, n=n, sn=sn, quadrant=quad)

                timg = trect.draw()
                score = util.rmsdiff(img, timg)
                # print quad, score
                if score <= best_score:
                    best_trect = trect
                    best_score = score

        return best_trect

    # return the perceived hue / luminance for now
    def draw(self):
        paper = Image.new('RGBA', (self.width, self.height))
        canvas = ImageDraw.Draw(paper)

        pw = 10 #(self.width/len(self.colors))/2

        # if random.randrange(2):
            # self.colors_secondary = list(reversed(self.colors_secondary))

        if len(self.colors)>=3:
            self.colors[1], self.colors[2] = self.colors[2], self.colors[1]

        """
        draw border square
        """
        width = pw
        for idx, color in enumerate(self.colors_secondary):
            paper.paste(color, [width*idx,width*idx, self.width-width*idx, self.height-width*idx])


        """
        draw triangles
        """
        x_offset = pw*(len(self.colors_secondary))+self.shrink
        y_offset = pw*(len(self.colors_secondary))+self.shrink
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







