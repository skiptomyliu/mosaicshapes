


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
    def __init__(self, size=(200,200), label=0):
        self.width = size[0]
        self.height = size[1]
        self.colors = [None]*4

        if label%3 == 0:
            self.colors = [(54, 9, 9), (54, 29, 9), (5, 32, 32), (7, 43, 7)]
            shuffle(self.colors)
            # self.colors[0] = (54, 9, 9)
            # self.colors[1] = (54, 29, 9)
            # self.colors[2] = (5, 32, 32)
            # self.colors[3] = (7, 43, 7)
        elif label%3 == 1:
            self.colors = [(24, 32, 63), (51, 20, 62), (17, 54, 57)]
            shuffle(self.colors)
        elif label%3 == 2:
            self.colors[0] = (20,0,20)
            self.colors[1] = (0,20,20)
            self.colors[2] = (20,20,0)
            self.colors[3] = (0,0,20)
            shuffle(self.colors)
        elif label%16 == 3:
            self.colors[0] = (100,0,0)
            self.colors[1] = (0,100,0)
            self.colors[2] = (0,0,100)
            self.colors[3] = (100,100,0)
        else:
            self.colors[0] = (55,55,55)
            self.colors[1] = (55,55,55)
            self.colors[2] = (55,55,55)
            self.colors[3] = (55,55,55)


    def draw(self, slope=-10000):
        paper = Image.new('RGBA', (self.width,self.height))

        canvas = ImageDraw.Draw(paper)
        width = 2
        for idx, color  in enumerate(self.colors):
            paper.paste(color, [width*idx,width*idx, self.width-width*idx, self.height-width*idx])

        # paper.show()
        # import pdb; pdb.set_trace()

        return paper







