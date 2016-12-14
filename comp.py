


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
                            # blue            green            red             orange
            self.colors = [(194,194,200), (202,218, 183), (223, 179, 181), (252, 195, 162)]
            shuffle(self.colors)

       
        elif label%3 == 1:
            # self.colors = [(24, 32, 63), (51, 20, 62), (17, 54, 57)]
            self.colors = [(54, 9, 9), (54, 29, 9), (5, 32, 32), (7, 43, 7)]
            shuffle(self.colors)


            
        # elif label%5 == 1:
        #     #light 1
        #     self.colors = [(251, 62, 135), (255, 179, 114), (248, 110, 132), (255, 161, 114)]
        #     shuffle(self.colors)
        # elif label%5 == 2:
        #     #dark 2
        #     # self.colors = [(24, 32, 63), (51, 20, 62), (17, 54, 57)]
        #     self.colors = [(54, 9, 9), (54, 29, 9), (5, 32, 32), (7, 43, 7)]
        #     shuffle(self.colors)
            
        # elif label%5 == 3:
        #     # highlight
        #     self.colors = [(248, 120, 192),(255, 233, 175),(255, 203, 175),(175, 225, 249)] 
        #     shuffle(self.colors)
        #     # import pdb; pdb.set_trace()

        else:
            self.colors = [(255, 122, 69),(240, 143, 211), (252, 173, 218),(97, 172, 216)]
            shuffle(self.colors)



    def draw(self, slope=-10000):
        paper = Image.new('RGBA', (self.width,self.height))

        canvas = ImageDraw.Draw(paper)
        width = 2
        count = 0
        for idx, color in enumerate(self.colors):
            paper.paste(color, [width*idx,width*idx, self.width-width*idx, self.height-width*idx])
            count += 1
            # if count>0:
                # break;

        # paper.show()
        # import pdb; pdb.set_trace()

        return paper







