


from PIL import Image, ImageDraw
import numpy as np
from colorpalette import ColorPalette
import random
import matplotlib.pyplot as plt
import util
from cell import Cell

class RectCell(Cell):
    def __init__(self, size=(200,200), csize=(200,200), base_color=(0,0,0), second_color=(0,0,0), n=4, sn=1):

        self.width = size[0]
        self.height = size[1]
        self.cwidth = csize[0]
        self.cheight = csize[1]
        self.base_color = base_color

        self.colors = Cell.gen_colors(base_color, n)
        self.colors_secondary = Cell.gen_colors(second_color,sn)


    @staticmethod
    def find_best(img, n=2, sn=2):
        second_color,base_color = ColorPalette.quantize_img(img, 2)

        color_combos = [[base_color, second_color], [second_color, base_color]]

        width,height = img.size
        best_rcell = None
        best_score = 10000

        #XXX:  hardcoded at 4 at moment...  pw*2 is the minimum csize
        # for w in range(int(width-10), width):
            # for h in range(4, height):
        w = width - 10
        h = height - 25
        for color_combo in color_combos:
            for i in range(2):
                h = w
                rcell = RectCell(size=(width,height), csize=(w,h), 
                    base_color=color_combo[0], second_color=color_combo[1], 
                    n=n, sn=sn)
                # if i:
                #     rcell.colors = list(reversed(rcell.colors))
                cimg = rcell.draw()
                score = util.rmsdiff(img, cimg)
                if score <= best_score:
                    best_rcell = rcell
                    best_score = score
                    # best_rcell.draw().show()
                    # import pdb; pdb.set_trace()

        return best_rcell

    # return the perceived hue / luminance for now
    def draw(self):
        paper = Image.new('RGBA', (self.width, self.height))
        canvas = ImageDraw.Draw(paper)

        pw = 6#(self.width/len(self.colors))/3
        if random.randrange(2):
            self.colors = list(reversed(self.colors))
            
        if len(self.colors)>=3:
            self.colors[1], self.colors[2] = self.colors[2], self.colors[1]

        """
        draw border square
        """
        for idx, color in enumerate(self.colors_secondary):
            paper.paste(color, [pw*idx,pw*idx, self.width-pw*idx, self.height-pw*idx])

        """
        draw rect
        """
        for idx, color in enumerate(self.colors):
            color = int(color[0]),int(color[1]),int(color[2])
            sx = int(round((self.width-self.cwidth)/2))
            sy = 0 +  len(self.colors)*pw # (self.height-self.cheight)/2
            ey = self.height - sy
            paper.paste(color, [sx + (pw*idx), sy+(pw*idx), sx+(self.cwidth-pw*idx)+1, ey-pw*idx])

        return paper







