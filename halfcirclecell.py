


from PIL import Image, ImageDraw
import numpy as np
from colorpalette import ColorPalette
import random
import util
from cell import Cell, Direction

class HalfCircleCell(Cell):
    def __init__(self, size=(200,200), base_color=(0,0,0), second_color=(0,0,0), 
        shrink=0, n=4, sn=1, direction=Direction.top):

        self.width = size[0]
        self.height = size[1]
        self.base_color = base_color

        self.colors = Cell.gen_colors(base_color, n)
        self.colors_secondary = Cell.gen_colors(second_color,sn)
        self.direction = direction
        self.shrink = shrink


    @staticmethod
    def find_best(img, n=2, sn=2):
        second_color,base_color = ColorPalette.quantize_img(img,2)
        color_combos = [[second_color,base_color], [base_color, second_color]]

        quads = [Direction.top, Direction.right, Direction.bottom, Direction.left]

        best_hcell = None
        best_score = 10000
        w,h = img.size
        for quad in quads:
            for color_combo in color_combos:
                hcell = HalfCircleCell(size=(w,h), 
                    base_color=color_combo[0], second_color=color_combo[1], 
                    shrink=0, n=n, sn=sn, direction=quad)

                himg = hcell.draw()
                score = util.rmsdiff(img, himg)
                if score <= best_score:
                    best_hcell = hcell
                    best_score = score

        return best_hcell

    def draw(self):
        # super sample by 4x
        N=4
        paper = Image.new('RGBA', (self.width*N, self.height*N))
        canvas = ImageDraw.Draw(paper, paper.mode)

        shortest = self.width if self.width < self.height else self.height
        pw = int(round(.5 * shortest * 1/(len(self.colors) + len(self.colors_secondary))))
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
            sdeg, edeg = (180, 0)
            sx = aidx*N + pw*idx*N
            ex = self.width*N
            ex-= (pw*idx*N)
            sy = aidx*N + pw*idx*N
            ey = self.height*N 
            ey-= pw*idx*N*2.5 + aidx*N*2
            canvas.pieslice([sx,sy,ex,ey], sdeg, edeg, fill=color, outline=None)

        if self.direction == Direction.top:
            pass
        elif self.direction ==  Direction.right:
            paper = paper.rotate(-90)
        elif self.direction ==  Direction.bottom:
            paper = paper.rotate(180)
        elif self.direction ==  Direction.left:
            paper = paper.rotate(90)

        del canvas
        paper.thumbnail((self.width, self.height))

        return paper

