


from PIL import Image, ImageDraw
import numpy as np
from colorpalette import ColorPalette
import random
import matplotlib.pyplot as plt
import util
from cell import Cell

class CircleCell(Cell):
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
        second_color,base_color = ColorPalette.quantize_img(img,2)
        color_combos = [[second_color,base_color], [base_color, second_color]]

        width,height = img.size
        best_ccell = None
        best_score = 10000

        #XXX:  hardcoded at 4 at moment...  pw*2 is the minimum csize
        for w in range(width-2, width):
            # for h in range(4, height):
            h = w
            for color_combo in color_combos:
                ccell = CircleCell(size=(width,height), csize=(w,h), base_color=color_combo[0], second_color=color_combo[1], n=n, sn=sn)
                cimg = ccell.draw()
                score = util.rmsdiff(img, cimg)
                if score <= best_score:
                    best_ccell = ccell
                    best_score = score

        return best_ccell

    # return the perceived hue / luminance for now
    def draw(self):
        # super sample by 4x
        N=4
        paper = Image.new('RGBA', (self.width*N, self.height*N))
        canvas = ImageDraw.Draw(paper, paper.mode)

        pw = 2 #(self.width/len(self.colors))/2
        if random.randrange(2):
            self.colors = list(reversed(self.colors))

        if len(self.colors)>=3:
            self.colors[1], self.colors[2] = self.colors[2], self.colors[1]

        """
        draw border square
        """
        for idx, color in enumerate(self.colors_secondary):
            paper.paste(color, [pw*idx*N,pw*idx*N, (self.width-pw*idx)*N, (self.height-pw*idx)*N])

        """
        draw circles
        """
        for idx, color in enumerate(self.colors):
            color = int(color[0]),int(color[1]),int(color[2])
            sx = (self.width-self.cwidth)/2
            sy = (self.height-self.cheight)/2
            canvas.ellipse([(sx + (pw*idx))*N, (sy+(pw*idx))*N, (sx+(self.cwidth-pw*idx))*N, (sy+(self.cheight-pw*idx))*N], fill=color)

        del canvas
        paper.thumbnail((self.width, self.height)) 

        return paper







