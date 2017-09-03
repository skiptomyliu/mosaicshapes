


from PIL import Image, ImageDraw
import util
from cell import Cell, Quadrant

class PieSliceCell(Cell):
    def __init__(self, size=(200,200), base_colors=[], second_colors=[], 
        shrink=0, quadrant=Quadrant.top_left):

        self.width = size[0]
        self.height = size[1]

        self.colors = base_colors 
        self.colors_secondary = second_colors
        # self.colors = Cell.gen_colors(base_color, n, colorful)
        # self.colors_secondary = Cell.gen_colors(second_color, sn, colorful)
        self.quadrant = quadrant
        self.shrink = shrink


    @staticmethod
    def find_best(img, base_colors=[], second_colors=[], N=2):
        color_combos = [[second_colors,base_colors], [base_colors, second_colors]]
        # color_combos = [[second_colors,base_colors]]
        
        quads = [Quadrant.top_left, Quadrant.top_right, Quadrant.bottom_left, Quadrant.bottom_right]

        best_img = None
        best_score = 10000
        w,h = img.size
        for quad in quads:
            for color_combo in color_combos:
                pcell = PieSliceCell(size=(w,h), 
                    base_colors=color_combo[0], second_colors=color_combo[1], 
                    shrink=0, quadrant=quad)

                pimg = pcell.draw(N=1)
                score = util.rmsdiff(img, pimg)
                if score <= best_score:
                    best_img = pcell#.draw(N=N)
                    best_score = score

        return best_img.draw(N=N), best_score

    def draw(self, N=2):
        # super sample by 3x
        n_width, n_height = int(self.width*N), int(self.height*N)
        paper = Image.new('RGBA', (n_width, n_height))
        canvas = ImageDraw.Draw(paper, paper.mode)

        shortest = n_width if n_width < n_height else n_height
        pw = int(round(.5 * shortest * 1/(len(self.colors) + len(self.colors_secondary))))
        # if random.randrange(2):
        #     self.colors = list(reversed(self.colors))

        if len(self.colors)>=3:
            self.colors[1], self.colors[2] = self.colors[2], self.colors[1]

        """
        draw border square
        """
        for idx, color in enumerate(self.colors_secondary):
            paper.paste(color, [pw*idx, pw*idx, (n_width-pw*idx), (n_height-pw*idx)])

        """
        draw pie slices
        """
        # Start with botom right quadrant drawing
        # self.shrink=3

        x_offset = (pw*(len(self.colors_secondary)/2)+self.shrink)
        y_offset = (pw*(len(self.colors_secondary)/2)+self.shrink)
        for idx, color in enumerate(self.colors):
            color = int(color[0]),int(color[1]),int(color[2])
            aidx = len(self.colors_secondary) + idx +1
            sdeg, edeg = (180, 270)
            sx = pw*idx*1.5+x_offset#+(aidx*2*N)
            ex = (n_width*2-pw*aidx)
            ex-= (pw*idx*2)
            sy = pw*idx+y_offset #+(aidx*2*N)
            ey = (n_height*2-pw*aidx)
            ey-= pw*idx*1.5
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

        # paper.thumbnail((self.width, self.height))

        return paper

