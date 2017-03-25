


from PIL import Image, ImageDraw
import util
from cell import Cell, Direction

class HalfCircleCell(Cell):
    def __init__(self, size=(200,200), base_color=(0,0,0), second_color=(0,0,0), 
        shrink=0, n=4, sn=1, direction=Direction.top, colorful=True):

        self.width = size[0]
        self.height = size[1]
        self.base_color = base_color

        self.colors = Cell.gen_colors(base_color, n, colorful)
        self.colors_secondary = Cell.gen_colors(second_color, sn, colorful)
        self.direction = direction
        self.shrink = shrink


    @staticmethod
    def find_best(img, n=2, sn=2, base_color=(0,0,0), second_color=(0,0,0), colorful=True):
        color_combos = [[second_color,base_color], [base_color, second_color]]

        quads = [Direction.top, Direction.right, Direction.bottom, Direction.left]

        best_img = None
        best_score = 10000
        w,h = img.size
        for quad in quads:
            for color_combo in color_combos:
                hcell = HalfCircleCell(size=(w,h), 
                    base_color=color_combo[0], second_color=color_combo[1], 
                    shrink=0, n=n, sn=sn, direction=quad, colorful=colorful)

                himg = hcell.draw(N=1)
                score = util.rmsdiff(img, himg)
                if score <= best_score:
                    best_img = hcell.draw(N=4)
                    best_score = score

        return best_img, best_score

    def draw(self, N=2):
        # super sample by 2x
        n_width, n_height = self.width*N, self.height*N
        paper = Image.new('RGBA', (n_width, n_height))
        canvas = ImageDraw.Draw(paper, paper.mode)

        shortest = n_width if n_width < n_height else n_height
        pw = int(round(.5 * shortest * 1/(len(self.colors) + len(self.colors_secondary))))
        pw = util.clamp_int(pw, 1, 10000)

        """
        draw border square
        """
        for idx, color in enumerate(self.colors_secondary):
            paper.paste(color, [pw*idx,pw*idx, (n_width-pw*idx), (n_height-pw*idx)])

        """
        draw pie slices
        """
        x_offset = 0#len(self.colors_secondary)*pw#N*(pw*(len(self.colors_secondary))+self.shrink)
        y_offset = x_offset #N*(pw*(len(self.colors_secondary))+self.shrink)
        for idx, color in enumerate(self.colors):
            color = int(color[0]),int(color[1]),int(color[2])
            aidx = 0#len(self.colors_secondary) + idx
            sdeg, edeg = (180, 0)
            sx = aidx + pw*idx + x_offset
            ex = n_width - x_offset
            ex-= (pw*idx)
            sy = aidx + pw*idx
            ey = n_height
            ey-= pw*idx*2.5 + aidx*2
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
        # paper.thumbnail((self.width, self.height))

        return paper

