


from PIL import Image, ImageDraw
import numpy as np
from colorpalette import ColorPalette
import random
import matplotlib.pyplot as plt
import util
from cell import Cell, Quadrant

class PieSliceCell(Cell):
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
    def find_best(img, n=2, sn=2):
        second_color,base_color = ColorPalette.quantize_img(img,2)
        color_combos = [[second_color,base_color], [base_color, second_color]]

        quads = [Quadrant.top_left, Quadrant.top_right, Quadrant.bottom_left, Quadrant.bottom_right]

        best_pcell = None
        best_score = 10000
        w,h = img.size
        for quad in quads:
            for color_combo in color_combos:
                pcell = PieSliceCell(size=(w,h), 
                    base_color=color_combo[0], second_color=color_combo[1], 
                    shrink=0, n=n, sn=sn, quadrant=quad)

                pimg = pcell.draw()
                score = util.rmsdiff(img, pimg)
                if score <= best_score:
                    best_pcell = pcell
                    best_score = score

        return best_pcell

    # return the perceived hue / luminance for now
    def draw(self):
        # super sample by 4x
        N=4
        paper = Image.new('RGBA', (self.width*N, self.height*N))
        canvas = ImageDraw.Draw(paper, paper.mode)

        pw = 5 #(self.width/len(self.colors))/2
        # if random.randrange(2):
        #     self.colors = list(reversed(self.colors))

        if len(self.colors)>=3:
            self.colors[1], self.colors[2] = self.colors[2], self.colors[1]

        """
        draw border square
        """
        for idx, color in enumerate(self.colors_secondary):
            paper.paste(color, [pw*idx*N,pw*idx*N, (self.width-pw*idx)*N, (self.height-pw*idx)*N])

        """
        draw pie slices
        """
        x_offset = N*(pw*(len(self.colors_secondary))+self.shrink)
        y_offset = N*(pw*(len(self.colors_secondary))+self.shrink)
        for idx, color in enumerate(self.colors):
            color = int(color[0]),int(color[1]),int(color[2])
            aidx = len(self.colors_secondary) + idx
            sdeg, edeg = (180, 270)
            sx = pw*idx*N+(aidx*2*N)
            ex = (self.width*2-pw*aidx)*N
            ex-= (pw*idx*N*2)
            sy = pw*idx*N+(aidx*2*N)
            ey = (self.height*2.0-pw*aidx)*N 
            ey-= pw*idx*N*2
            canvas.pieslice([sx,sy,ex,ey], sdeg, edeg, fill=color, outline=None)

        if self.quadrant == Quadrant.top_right:
            paper = paper.rotate(90)
        elif self.quadrant ==  Quadrant.top_left:
            paper = paper.rotate(90*2)
        elif self.quadrant ==  Quadrant.bottom_right:
            pass
        elif self.quadrant ==  Quadrant.bottom_left:
            paper = paper.rotate(90*3)
        del canvas
        paper.thumbnail((self.width, self.height))

        return paper







