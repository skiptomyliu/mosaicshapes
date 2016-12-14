


from PIL import Image, ImageDraw
import numpy as np
# from numpy import random
import random
import matplotlib.pyplot as plt
from skimage.transform import PiecewiseAffineTransform, warp
import scipy
from scipy.misc import toimage
from random import shuffle
import colorsys

import util


"""
map shades to different color palettes  
"""


class CompColor():
    def __init__(self, size=(200,200), base_color=(0,0,0)):
        self.width = size[0]
        self.height = size[1]
        self.base_color = base_color
        self.colors = []

        self.random_colors = self.__random_color()

        # Initial base colors to initialize with:



        # if label%4 == 1:
        #                     # blue            green            red             orange
        #     self.colors = [(194,194,200), (202,218, 183), (223, 179, 181), (252, 195, 162)]
        #     shuffle(self.colors)

    def __random_color(self):
        salmon = (230,115,100)
        pink = (227, 151, 184)
        l_blue = (80,155,195)
        red = (205,40,60)
        purple = (130,118,154)
        l_green = (177,181,107)
        orange = (225,97,55)
        yellow = (250,193,67)
        colors = [salmon, pink, l_blue, red, purple, l_green, orange, yellow]
        shuffle(colors)
        return colors 
        # return colors[0]

    def correct(self, target_color):
        # first pass
        target_lum = util.luminance(target_color[0], target_color[1], target_color[2])
        if len(self.colors) <= 0:
            rc = self.random_colors.pop(0)
            new_lum = util.luminance(rc[0], rc[1], rc[2])
            if new_lum > target_lum:
                rc = util.shade_to_lum(rc, target_lum)
            elif new_lum < target_lum:
                rc = util.tint_to_lum(rc, target_lum-20)
            self.colors.append(rc)

        # second pass
        elif len(self.colors) == 1:

        else:
            pass

    def draw(self, slope=-10000):
        paper = Image.new('RGBA', (self.width, self.height))

        canvas = ImageDraw.Draw(paper)
        width = 3
        count = 0
        for idx, color in enumerate(self.colors):
            paper.paste(color, [width*idx,width*idx, self.width-width*idx, self.height-width*idx])
            # if count>0:
                # break;

        return paper







