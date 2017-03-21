


from PIL import Image, ImageDraw
import random
from random import shuffle
import colorsys
from cell import Cell
import util


"""

- triangle *
- pie slice
- multiple boxes for grid again (2x1,3x2, etc.)  Apply for edges.   Random for others?  Or only edges
- choosing between triangle and pie slice should measure against "closeness" to og_image.
- create a slimmer circle.  Done by using a smaller rect inside a rect
- need fg,bg rect for edges... or just use the elongated circles

"""


class CompColor(Cell):
    def __init__(self, size=(200,200), base_color=(0,0,0), n=4, colorful=True):
        self.width = size[0]
        self.height = size[1]
        self.base_color = base_color
        self.colors = []
        # self.colors = CompColor.gen_colors_c(base_color, random.randint(2,n+1))
        # self.colors = CompColor.gen_colors(base_color, random.randint(2,n+1))

        s=3 #xxx: this was set to 2 before
        self.colors = Cell.gen_colors(base_color, random.randint(s,n+1), colorful)

    @staticmethod
    def find_best(img, n=2, sn=2):
        pass

    # return the perceived hue / luminance for now
    def avg_lum(self, colors):
        cur_lum = 0
        for color in colors:
             cur_lum += util.luminance(color[0], color[1], color[2])

        return round(cur_lum / len(self.colors), 2)

    def correct(self, target_color):
        # first pass
        target_lum = util.luminance(target_color[0], target_color[1], target_color[2])
        if len(self.colors) <= 0:
            rc = self.random_colors.pop(0)
            new_lum = util.luminance(rc[0], rc[1], rc[2])
            if new_lum > target_lum:
                rc = util.shade_to_lum(rc, target_lum)
            elif new_lum < target_lum:
                rc = util.tint_to_lum(rc, target_lum)
            self.colors.append(rc)

        # second pass
        elif len(self.colors) == 1:
            rc = self.random_colors.pop(0)
            self.colors.append(rc)
        elif len(self.colors) == 2:
            rc = self.random_colors.pop(0)

            # if self.avg_hue(self.colors + [rc]) > target_lum:
            #     rc = util.shade_to_lum(rc, target_lum)
            if self.avg_lum(self.colors + [rc]) < target_lum:
                rc = util.tint_to_lums(rc, self.colors, target_lum)
                self.colors.append(rc)
            pass


    # Draws a rect and then a circle inside rect
    def draw_circle(self, N):
        width = (self.width/len(self.colors))/random.randint(2,2) # line width of circles
        stretch = 0 
        rect_paper = Image.new('RGBA', (self.width*N, self.height*N))
        rect_canvas = ImageDraw.Draw(rect_paper, rect_paper.mode)
        
        # if len(self.colors)>=3:
            # self.colors[1], self.colors[2] = self.colors[2], self.colors[1]

        for idx, color in enumerate(self.colors):
            color = int(color[0]),int(color[1]),int(color[2])
            x = width*idx*N
            y = width*idx*N
            ex = (self.width-width*idx)*N
            ey = (self.height-width*idx)*N
            rect_paper.paste(color, [x,y, ex, ey])

        circle_paper = Image.new('RGBA', (self.width*N, self.height*N))
        circle_canvas = ImageDraw.Draw(circle_paper, circle_paper.mode)


        for idx, color in enumerate(self.colors):
            color = int(color[0]),int(color[1]),int(color[2])
            x = (width*idx+stretch)*N + width/2*(len(self.base_color)-1)*N
            y = width*idx*N #+ width*(len(self.base_color)-1.5)*N
            ex = (self.width-width*idx-stretch)*N - width/2*(len(self.base_color)-1)*N
            ey = (self.height-width*idx)*N #- width*(len(self.base_color)-1.5)*N
            circle_canvas.ellipse([x, y, ex, ey], fill=color)

        # circle_paper = circle_paper.rotate(45*random.randint(0, 6))
        circle_paper = circle_paper.rotate(random.randint(0, 359))
        rect_paper.paste(circle_paper,(0,0), circle_paper)

        del rect_canvas
        del circle_canvas
        # rect_paper.thumbnail((self.width, self.height)) 
        return rect_paper

    # Draw rect only
    def draw_rect(self,N):
        paper = Image.new('RGBA', (self.width*N, self.height*N))
        canvas = ImageDraw.Draw(paper)

        width = (self.width/len(self.colors))/2
        for idx, color in enumerate(self.colors):
            color = int(color[0]),int(color[1]),int(color[2])
            paper.paste(color, [width*idx*N,width*idx*N, (self.width-width*idx)*N, (self.height-width*idx)*N])

        return paper

    def draw(self, N=2):
        if random.getrandbits(1): #XXX: Change to faster
            shape = self.draw_circle(N)
        else:
            shape = self.draw_rect(N)

        return shape




