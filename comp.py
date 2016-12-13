


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

    def __init__(self, size=(200,200), fg_color=(180,0,200), bg_color=(255,0,255)):
        self.width = size[0]
        self.height = size[1]
        self.color = fg_color
        self.fg_color = fg_color 
        self.bg_color = bg_color
        self.num_circles = 4
        self.warp_height = .04*np.random.random()

        self.sincos = np.cos if bool(random.getrandbits(1)) else np.sin

    def __paint_circles(self):
        pass


    def draw(self, slope=-10000):
        show_image = True
        CIRCLE_SIZE = max(self.width, self.height)
       
        paper = Image.new('RGBA', (self.width,self.height))

        # 1st color
         # Set up canvas where the circle will be pasted on
        r,g,b = self.fg_color
        c,m,y,k = util.rgb_to_cmyk(r,g,b)


        canvas = ImageDraw.Draw(paper)
        

        r,g,b = int(r), int(g), int(b)
        cr, cg, cb = util.complement(r,g,b)

        # paper.paste((r,g,b), [0,0,self.width,self.height])
        # paper.paste((cr,cg,cb), [0,0,self.width,self.height])
        # paper.show()
        # import pdb; pdb.set_trace()

        return paper







