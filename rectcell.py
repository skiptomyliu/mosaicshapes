


from PIL import Image, ImageDraw
import random
import util
from cell import Cell


"""
XXX: ciwdth and cheight not currently utilized 
"""
class RectCell(Cell):
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
        color_combos = [[base_color, second_color], [second_color, base_color]]

        width,height = img.size
        best_img = None
        best_score = 10000

        w = width 
        h = height

        # XXX: will cause probs if image size is less than 10 pixels
        for w in range(width-1, width):
            for h in range(height-1, height):

                for color_combo in color_combos:
                    for i in range(2):
                        h = w
                        rcell = RectCell(size=(width,height), csize=(w,h), 
                            base_color=color_combo[0], second_color=color_combo[1], 
                            n=n, sn=sn, colorful=colorful)

                        cimg = rcell.draw(N=1)
                        score = util.rmsdiff(img, cimg)
                        if score <= best_score:
                            best_img = rcell.draw(N=2)
                            best_score = score

        return best_img, best_score

    # return the perceived hue / luminance for now
    def draw(self, N=2):
        paper = Image.new('RGBA', (self.width*N, self.height*N))
        canvas = ImageDraw.Draw(paper)

        pw = 4#(self.width/len(self.colors))/3
        shortest = self.width if self.width < self.height else self.height
        pw = int(round(.5 * shortest * 1/(len(self.colors) + len(self.colors_secondary))))

        """
        draw border square
        """
        for idx, color in enumerate(self.colors_secondary):
            paper.paste(color, [pw*idx*N,pw*idx*N, (self.width-pw*idx)*N, (self.height-pw*idx)*N])

        """
        draw rect
        """
        for idx, color in enumerate(self.colors):
            color = int(color[0]),int(color[1]),int(color[2])
            sx = int(round((len(self.colors_secondary))*pw))
            # sx = int(round(len(self.colors)*pw/2))
            sx += (pw*idx)
            # sy = int(round(len(self.colors)*pw/2))
            sy = int(round(len(self.colors_secondary)*pw))
            sy += (pw*idx)
            ex = self.width - sx
            ey = self.height - sy
            paper.paste(color, [sx*N, sy*N, ex*N, ey*N])

        return paper







