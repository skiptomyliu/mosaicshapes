

from PIL import Image, ImageDraw, ImageOps
import numpy as np
from colorpalette import ColorPalette
import util
from cell import Cell, Quadrant

"""

- triangle
- pie slice
- multiple boxes for grid again
- choosing between triangle and pie slice should measure against "closeness" to og_image.


xxx: 3/25, shrink is not implemented
"""


class TriangleCell(Cell):
    def __init__(self, size=(200, 200), base_colors=[], second_colors=[],
                 shrink=0, quadrant=Quadrant.top_left):

        self.width = size[0]
        self.height = size[1]

        self.colors = base_colors
        self.colors_secondary = second_colors

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

    @staticmethod
    def find_best(img, base_colors=[], second_colors=[], N=2):
        color_combos = [[second_colors, base_colors], [base_colors, second_colors]]
        # color_combos = [[second_colors,base_colors]]
        quads = [Quadrant.top_left, Quadrant.top_right, Quadrant.bottom_left, Quadrant.bottom_right]

        w, h = img.size
        best_img = None
        best_score = 10000
        for quad in quads:
            for color_combo in color_combos:
                trect = TriangleCell(size=(w, h),
                                     base_colors=color_combo[0],
                                     second_colors=color_combo[1],
                                     shrink=0,
                                     quadrant=quad)

                timg = trect.draw(N=1)
                score = util.rmsdiff(img, timg)
                if score <= best_score:
                    best_img = trect
                    best_score = score

        return best_img.draw(N=N), best_score

    # return the perceived hue / luminance for now
    def draw(self, N=2):
        # pw = 4 #(self.width/len(self.colors))/2
        n_width, n_height = int(self.width*N), int(self.height*N)
        shortest = n_width if n_width < n_height else n_height
        pw = int(round(.5 * .5 * shortest * 1/(len(self.colors) + len(self.colors_secondary))))
        pw = util.clamp_int(pw, 1, 10000)
        # pw = 6
        # print pw
        # import pdb; pdb.set_trace()
        # pw = 1
        # print pw
        # import pdb; pdb.set_trace()
        paper = Image.new('RGBA', (n_width, n_height))
        canvas = ImageDraw.Draw(paper, paper.mode)

        """
        draw border square
        """
        for idx, color in enumerate(self.colors_secondary):
            paper.paste(color, [pw*idx, pw*idx, (n_width-pw*idx), (n_height-pw*idx)])

        """
        draw triangles
        """

        x_offset = pw*(len(self.colors_secondary))
        y_offset = pw*(len(self.colors_secondary))

        for idx, color in enumerate(self.colors):
            color = int(color[0]), int(color[1]), int(color[2])
            width, height = n_width-pw*idx, n_height-pw*idx
            sx = (pw*idx + x_offset)
            sy = (pw*idx + y_offset)

            # sx = int(round(len(self.colors)*pw/2.0))
            # sx += (pw*idx)
            ex = n_width - sx
            coord = [(sx + pw*idx),
                     sy,
                     (ex, sy),
                     (ex, (height-sy-idx))]
            canvas.polygon(coord, fill=color)

        if self.quadrant == Quadrant.top_right:
            pass
        elif self.quadrant == Quadrant.top_left:
            paper = paper.rotate(90)
        elif self.quadrant == Quadrant.bottom_right:
            paper = paper.rotate(-90)
        elif self.quadrant == Quadrant.bottom_left:
            paper = paper.rotate(180)

        del canvas
        # paper.thumbnail((self.width, self.height))

        return paper
