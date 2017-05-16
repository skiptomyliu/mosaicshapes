

import numpy as np
from numpy.random import randint
from random import shuffle
import random
import util

class ColorType(object):
    kNORMAL = 0
    kCOLORFUL = 1
    kANALOGOUS = 2

class GenColor(object):

    @staticmethod
    def gen_colors(base_color, n, colorful=ColorType.kNORMAL):
        if colorful == ColorType.kCOLORFUL:
            return GenColor.gen_colorful(base_color, n)
        elif colorful == ColorType.kNORMAL:
            return GenColor.gen_colors_og(base_color, n)
        elif colorful == ColorType.kANALOGOUS:
            return GenColor.gen_analogous(base_color, n)


    #XXX: todo another analogous color palette
    @staticmethod
    def gen_analogous(base_color, n):
        r,g,b = base_color
        adj_colors = util.adjacent_colors(base_color, d=20/360.0)

        c1 = GenColor.gen_colors_og(adj_colors[0], 1)
        c2 = GenColor.gen_colors_og(adj_colors[1], 1)

        all_colors = c1 + c2 

        if n==1:
            all_colors.append(base_color)

        all_colors.append(base_color)
        shuffle(all_colors)

        return all_colors

    @staticmethod
    def gen_colorful(base_color, n):
        r,g,b = base_color
        adj_colors = util.adjacent_colors(base_color)
        complement_colors = [util.complement(c[0],c[1],c[2]) for c in adj_colors]

        # shuffle(complement_colors)
        c1 = GenColor.gen_colors_og(adj_colors[0], 1)
        c2 = GenColor.gen_colors_og(adj_colors[1], 1)
        # c1 = GenColor.gen_colors_og(adj_colors[0], random.randint(1,1))
        # c2 = GenColor.gen_colors_og(adj_colors[1], random.randint(1,1))

        # option for non complement
        all_colors = c1 + c2 #+ complement_colors
        # shuffle(all_colors)
        if n==1:
            all_colors.append(base_color)

        #XXX: The complementary colors likely should be the main middle
        # it occupies too much space, it should be accentuating
        # base + adj colors should be more towards middle
        # all_colors = all_colors[:n-1]
        all_colors.append(base_color)
        shuffle(all_colors)

        # all_colors.insert(randint(1,len(all_colors)-1), complement_colors[0])
        # Add 30% complement colors
        if randint(0,101)>30:
            all_colors.insert(randint(1, len(all_colors)), complement_colors[randint(0,2)])

        return all_colors

    @staticmethod
    def gen_colors_og(base_color, n):
        colors = []
        if n==1:
            if isinstance(base_color, (np.ndarray, np.generic)):
                base_color = tuple(base_color.astype(int))
            colors.append(base_color)
        else:   
            # maximum distance between all colors combined
            distance = 25
            colors = []

            r,g,b = base_color
            quad = 1 if util.luminance(r,g,b) > 100 else 0

            for i in range(-n/2+quad, n/2+quad):
                color = np.asarray(base_color) + (i)*distance/float(n)
                color[0] = util.clamp_int(color[0], 0, 255) #R
                color[1] = util.clamp_int(color[1], 0, 255) #G
                color[2] = util.clamp_int(color[2], 0, 255) #B
                color = tuple(color.astype(int))
                colors.append(color)


            if not random.getrandbits(1):
                shuffle(colors)
            else:
                if len(colors)>=3:
                    colors[1], colors[2] = colors[2], colors[1]

        return colors