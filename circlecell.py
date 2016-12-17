


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
        fg,bg = ColorPalette.average_colors(img,n)
        second_color = (fg*255).astype(int)
        base_color = (bg*255).astype(int)

        width,height = img.size
        best_ccell = None
        best_score = 10000

        # for quad in quads:
        for w in range(40, width):
            for h in range(40, height):

                ccell = CircleCell(size=(width,height), csize=(w,h), base_color=base_color, second_color=second_color, n=n, sn=sn)
                timg = ccell.draw()
                timg.show()
                # import pdb; pdb.set_trace()
                score = util.rmsdiff(img, timg)
                # print quad, score
                if score <= best_score:
                    best_ccell = ccell
                    best_score = score

        return best_ccell

    # return the perceived hue / luminance for now
    def draw(self):
        paper = Image.new('RGBA', (self.width, self.height))
        canvas = ImageDraw.Draw(paper)

        pw = 2 #(self.width/len(self.colors))/2
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
        draw circles
        """
        for idx, color in enumerate(self.colors):
            color = int(color[0]),int(color[1]),int(color[2])

            sx = (self.width-self.cwidth)/2
            sy = (self.height-self.cheight)/2
            print [sx + (pw*idx),sy+(pw*idx), sx+(self.cwidth-pw*idx), sy+(self.cheight-pw*idx)]
            canvas.ellipse([sx + (pw*idx), sy+(pw*idx), sx+(self.cwidth-pw*idx), sy+(self.cheight-pw*idx)], fill=color)

        return paper







