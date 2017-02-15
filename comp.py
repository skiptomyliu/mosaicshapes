


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
        self.colors = Cell.gen_colors(base_color, random.randint(2,n+1), colorful)
        # self.random_colors = self.__random_color()

        # Initial base colors to initialize with:

        # if label%4 == 1:
        #                     # blue            green            red             orange
        #     self.colors = [(194,194,200), (202,218, 183), (223, 179, 181), (252, 195, 162)]
        #     shuffle(self.colors)

    @staticmethod
    def find_best(img, n=2, sn=2):
        pass


    # @staticmethod 
    # def gen_colors_c(base_color, n):
    #     r,g,b = base_color
    #     adj_colors = util.adjacent_colors(base_color)
    #     complement_colors = [util.complement(r,g,b) for c in adj_colors]

    #     # shuffle(adj_colors)
    #     shuffle(complement_colors)


    #     # all_colors = [adj_colors[0]] + [complement_colors[0]] + [base_color]
    #     c1 = CompColor.gen_colors(adj_colors[0], random.randint(2,2))
    #     c2 = CompColor.gen_colors(adj_colors[1], random.randint(2,2))
    #     all_colors = c1 + c2

    #     # import pdb; pdb.set_trace()
    #     if n==1:
    #         colors.append(base_color)
    #     else:
    #         shuffle(all_colors)
            
    #     return all_colors




# adjacent_colors
# complement

    # @staticmethod
    # def gen_colors(base_color, n):
    #     # print "in here"
    #     deg = 30/360.0
    #     colors = []
    #     if n==1:
    #         colors.append(base_color)
    #     else:   
    #         # minimum distance of twenty values
    #         distance = 40
    #         colors = []

    #         r,g,b = base_color
    #         quad = 1 if util.luminance(r,g,b) > 100 else 0
    #         for i in range(-n/2+quad, n/2+quad):
    #             color = np.asarray(base_color) + (i)*distance/float(n)
    #             color[0] = util.clamp_int(color[0], 0, 255) #R
    #             color[1] = util.clamp_int(color[1], 0, 255) #G
    #             color[2] = util.clamp_int(color[2], 0, 255) #B
    #             color = tuple(color)
    #             colors.append(color)


    #     return colors

    def __random_color(self):
        g0 = (220, 220, 220)
        g1 = (153, 153, 153)
        g2 = (119, 119, 119)
        g3 = (85, 85,  85) 
        g4 = (51, 51,  51)
        g5 = (17, 17,  17)  
        colors = [g0,g1,g2,g3,g4,g5]
        shuffle(colors)
        return colors

    # def __random_color(self):
    #     salmon = (230,115,100)
    #     pink = (227, 151, 184)
    #     l_blue = (80,155,195)
    #     red = (205,40,60)
    #     purple = (130,118,154)
    #     l_green = (177,181,107)
    #     orange = (225,97,55)
    #     yellow = (250,193,67)
    #     colors = [salmon, pink, l_blue, red, purple, l_green, orange, yellow]
    #     shuffle(colors)
    #     return colors 
    #     # return colors[0]

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


    def draw_circle(self):
        width = (self.width/len(self.colors))/random.randint(2,4)
        stretch = 0 #self.width/7
        N=3
        rect_paper = Image.new('RGBA', (self.width*N, self.height*N))
        rect_canvas = ImageDraw.Draw(rect_paper, rect_paper.mode)
        
        if len(self.colors)>=3:
            self.colors[1], self.colors[2] = self.colors[2], self.colors[1]

        for idx, color in enumerate(self.colors):
            color = int(color[0]),int(color[1]),int(color[2])
            x = width*idx*N
            y = width*idx*N
            ex = (self.width-width*idx)*N
            ey = (self.height-width*idx)*N
            rect_paper.paste(color, [x,y, ex, ey])


        circle_paper = Image.new('RGBA', (self.width*N, self.height*N))
        circle_canvas = ImageDraw.Draw(circle_paper, circle_paper.mode)

        self.colors = list(reversed(self.colors))
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
        rect_paper.thumbnail((self.width, self.height)) 
        return rect_paper

    def draw_rect(self):
        paper = Image.new('RGBA', (self.width, self.height))
        canvas = ImageDraw.Draw(paper)

        width = (self.width/len(self.colors))/2

        if random.randrange(2):
            self.colors = list(reversed(self.colors))

        if len(self.colors)>=3:
            self.colors[1], self.colors[2] = self.colors[2], self.colors[1]

        for idx, color in enumerate(self.colors):
            color = int(color[0]),int(color[1]),int(color[2])
            paper.paste(color, [width*idx,width*idx, self.width-width*idx, self.height-width*idx])
        # paper.show()

        return paper


    def draw(self):
        if random.randrange(0,2):
            shape = self.draw_circle()
        else:
            shape = self.draw_rect()

        return shape




