


from PIL import Image, ImageDraw
import random
import util
from cell import Cell

class CircleCell(Cell):
    def __init__(self, size=(200,200), csize=(200,200), 
        base_color=(0,0,0), second_color=(0,0,0), n=4, sn=1, colorful=True):

        self.width = size[0]
        self.height = size[1]
        self.cwidth = csize[0]
        self.cheight = csize[1]
        self.base_color = base_color

        self.colors = Cell.gen_colors(base_color, n, colorful)
        self.colors_secondary = Cell.gen_colors(second_color,sn, colorful)


    @staticmethod
    def find_best(img, n=2, sn=2, base_color=(0,0,0), second_color=(0,0,0), colorful=True):
        color_combos = [[second_color,base_color], [base_color, second_color]]

        width,height = img.size
        best_ccell = None
        best_score = 10000

        w = width
        h = height  

        dynamic = width if height > width else height
        #XXX:  May need to double check these on smaller images:
        step = int((dynamic-dynamic/2)/(4.0))
        step = 1 if not step else step
        for d in range(dynamic/2, dynamic, step):
            # d = dynamic
            for color_combo in color_combos:
                if height > width:
                    ccell = CircleCell(size=(width,height), csize=(d,height), 
                        base_color=color_combo[0], second_color=color_combo[1], 
                        n=n, sn=sn, colorful=colorful)
                else:
                    ccell = CircleCell(size=(width,height), csize=(width,d), 
                        base_color=color_combo[0], second_color=color_combo[1], 
                        n=n, sn=sn, colorful=colorful)
                cimg = ccell.draw()
                score = util.rmsdiff(img, cimg)
                if score <= best_score:
                    best_ccell = ccell
                    best_score = score

            return best_ccell

    # return the perceived hue / luminance for now
    def draw(self):
        # super sample by 2x
        N=3
        paper = Image.new('RGBA', (self.width*N, self.height*N))
        canvas = ImageDraw.Draw(paper, paper.mode)

        pw = 4 #(self.width/len(self.colors))/2
        shortest = self.width if self.width < self.height else self.height
        pw = int(round(.2 * shortest * 1/(len(self.colors) + len(self.colors_secondary))))

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







