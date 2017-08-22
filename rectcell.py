

from PIL import Image, ImageDraw
import random
import util
from cell import Cell


"""
XXX: ciwdth and cheight not currently utilized
"""


class RectCell(Cell):
    def __init__(self, size=(200, 200), csize=(200, 200),
                 base_colors=[], second_colors=[]):

        self.width = size[0]
        self.height = size[1]
        self.cwidth = csize[0]
        self.cheight = csize[1]

        self.colors = base_colors
        self.colors_secondary = second_colors

    @staticmethod
    def find_best(img, n=2, sn=2, base_colors=[], second_colors=[], N=2):
        color_combos = [[base_colors, second_colors], [second_colors, base_colors]]

        width, height = img.size
        best_img = None
        best_score = 10000

        w = width
        h = height

        # XXX: will cause probs if image size is less than 10 pixels
        # for w in range(width-1, width):
            # for h in range(height-1, height):
        for color_combo in color_combos:
            # h = w
            rcell = RectCell(size=(width, height), csize=(width, height),
                             base_colors=color_combo[0], second_colors=color_combo[1])

            cimg = rcell.draw(N=1)
            score = util.rmsdiff(img, cimg)
            if score <= best_score:
                best_img = rcell
                best_score = score

        return best_img.draw(N=N), best_score

    # return the perceived hue / luminance for now
    def draw(self, N=2):
        n_width, n_height = int(self.width*N), int(self.height*N)
        paper = Image.new('RGBA', (n_width, n_height))
        canvas = ImageDraw.Draw(paper)

        # pw = 4 #(self.width/len(self.colors))/3
        shortest = n_width if n_width < n_height else n_height
        pw = int(round(.5 * shortest * 1/(len(self.colors) + len(self.colors_secondary))))
        # print pw
        # import pdb; pdb.set_trace()
        """
        draw border square
        """
        for idx, color in enumerate(self.colors_secondary):
            paper.paste(color, [pw*idx, pw*idx, n_width-pw*idx, n_height-pw*idx])

        """
        draw rect
        """
        for idx, color in enumerate(self.colors):
            color = int(color[0]), int(color[1]), int(color[2])
            sx = int(round((len(self.colors_secondary))*pw))
            sx += (pw*idx)
            sy = int(round(len(self.colors_secondary)*pw))
            sy += (pw*idx)
            ex = n_width - sx
            ey = n_height - sy
            paper.paste(color, [sx, sy, ex, ey])

        return paper
