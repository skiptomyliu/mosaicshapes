

from PIL import Image, ImageDraw
from cell import Cell
import random
import util


class CircleCell(Cell):
    def __init__(self, size=(200, 200), csize=(200, 200),
                 base_colors=[], second_colors=[]):

        self.width = size[0]
        self.height = size[1]
        self.cwidth = csize[0]
        self.cheight = csize[1]
        self.colors = base_colors  # Cell.gen_colors(base_color, n, colorful)
        self.colors_secondary = second_colors  # Cell.gen_colors(second_color,sn, colorful)

    @staticmethod
    def find_best(img, n=2, sn=2, base_colors=[], second_colors=[], colorful=True, N=2):
        color_combos = [[second_colors, base_colors], [base_colors, second_colors]]

        width, height = img.size
        best_img = None
        best_score = 10000

        w = width
        h = height

        dynamic = width if height > width else height
        # XXX:  May need to double check these on smaller images:
        step = int((dynamic-dynamic/2)/(4.0))
        step = 1 if not step else step
        for d in range(dynamic/2, dynamic, step):
            # d = dynamic
            for color_combo in color_combos:
                if height > width:
                    ccell = CircleCell(size=(width, height),
                                       csize=(d, height),
                                       base_colors=color_combo[0],
                                       second_colors=color_combo[1])
                else:
                    ccell = CircleCell(size=(width, height),
                                       csize=(width, d),
                                       base_colors=color_combo[0],
                                       second_colors=color_combo[1])

                cimg = ccell.draw(N=1)
                score = util.rmsdiff(img, cimg)

                if score <= best_score:
                    best_img = ccell
                    best_score = score

            return (best_img.draw(N=N), best_score)

    # return the perceived hue / luminance for now
    def draw(self, N=2):
        # super sample by 2x
        # XXX:  This may need double checking
        n_width, n_height = int(self.width*N), int(self.height*N)
        n_cwidth, n_cheight = int(self.cwidth*N), int(self.cheight*N)
        paper = Image.new('RGBA', (n_width, n_height))
        canvas = ImageDraw.Draw(paper, paper.mode)

        # pw = 4 #(self.width/len(self.colors))/2
        shortest = n_width if n_width < n_height else n_height
        pw = int(round(.2 * shortest * 1/(len(self.colors) + len(self.colors_secondary))))
        pw = util.clamp_int(pw, 1, 10000)

        """
        draw border square
        """
        for idx, color in enumerate(self.colors_secondary):
            paper.paste(color, [pw*idx, pw*idx, n_width-pw*idx, n_height-pw*idx])

        """
        draw circles
        """
        for idx, color in enumerate(self.colors):
            color = int(color[0]), int(color[1]), int(color[2])
            sx = (n_width-n_cwidth)/2
            sy = (n_height-n_cheight)/2
            canvas.ellipse([(sx + (pw*idx)),
                           (sy+(pw*idx)),
                           (sx+(n_cwidth-pw*idx)),
                           (sy+(n_cheight-pw*idx))], fill=color)

        del canvas
        # paper.thumbnail((self.width, self.height))

        return paper







