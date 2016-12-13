

import util 

from PIL import Image, ImageDraw
from warped import Warped
from comp import CompColor
from skimage.color import rgb2grey
from skimage import io, feature
import matplotlib.pyplot as plt
import numpy as np
from enum import Enum
from colorpalette import ColorPalette
import random 

# remove later?
class Slope(Enum):
    uphill = 1
    downhill = 2
    horizontal = 3
    vertical = 4
    

"""
Sample color palette multiple times?
"""
class Grid():
    def __init__(self, imgpath):

        self.og_image = Image.open(imgpath)
        self.image = Image.new('RGB', self.og_image.size)
        self.draw = ImageDraw.Draw(self.image, 'RGBA')

        self.img_edges = feature.canny(rgb2grey(io.imread(imgpath)), sigma=3)

        self.width,self.height = self.image.size
        self.pixels = 10
        self.grid_status = np.zeros([self.width/self.pixels, self.height/self.pixels])
        # self.color_palette = ColorPalette("./examples/pink.JPEG", 2)
        self.color_palette = ColorPalette(imgpath, 3)
        # plt.imshow(self.img_edges, cmap=plt.cm.gray)
        # plt.show()

    # By default we occupy one cell at a time.  x_total is number of additional horizontal
    # cells to occupy.  Vertical is number of additional vertical cells
    def occupy(self, x, y, x_total=1, y_total=1):
        for i in range(x_total):
            for j in range(y_total):
                if  x+i < self.width/self.pixels and y+j < self.height/self.pixels:
                    self.grid_status[x+i][y+j] = 1


    # Test vertical expansion
    def is_occupied(self, x, y):
        return self.grid_status[x][y] == 1

    def get_slope(self, img_seg):
        # if len(img_seg[img_seg==True]) > len(img_seg[img_seg==False])/50:
        if len(img_seg[img_seg==True]):
            x,y = np.where(img_seg==True)

            slope,_ = np.polyfit(x,y,1)

            if np.isnan(slope):
                return None

            return slope


    def warp(self):
        width,height = self.image.size
        print width,height
        pix = self.pixels

        for w in range(width/pix):
            for h in range(height/pix):
                if not self.is_occupied(w,h):

                    if random.randint(0,50)==1:
                        pix_w, pix_h = (pix*2, pix*1)
                    elif random.randint(0,50)==1:
                        pix_w, pix_h = (pix, pix*2)
                    else:
                        pix_w, pix_h = (pix, pix)

                    # create rect coords:
                    x,y = w*pix, h*pix
                    rect_coords = [
                        x, y, 
                        util.clamp_int(x+pix_w, 0, width), util.clamp_int(y+pix_h, 0, height)
                    ]
                    # img_seg = self.img_edges[y:y+pix_w,x:x+pix_h]
                    # slope = self.get_slope(img_seg)
                    slope = None
                    
                    if slope:
                        pass
                        # x_line,y_line = np.where(img_seg==True)
                        # prim_color = util.average_color_pixels(self.og_image, zip(x_line+x, y_line+y))

                        # x_bg,y_bg = np.where(img_seg==False)
                        # bg_color = util.average_color_pixels(self.og_image, zip(x_bg+x,y_bg+y))

                        # warped_rect = Warped(size=(pix,pix), fg_color=prim_color, bg_color=bg_color)
                        # img = warped_rect.draw(slope)

                        # # t_rect = TriangleRect(size=(pix,pix), fg_color=prim_color, bg_color=bg_color)
                        # # img = t_rect.draw(slope)

                        # self.image.paste(img, (w*pix,h*pix))
                        # self.og_image.paste(img, (w*pix,h*pix))

                    else:
                        color = util.average_color(self.og_image, rect=rect_coords)
                        # color = self.color_palette.translate_color(color)
                        color = np.asarray(color)/float(255)
                        color = color.reshape(1,-1)
                        label = self.color_palette.kmeans.predict(color)
                        # import pdb; pdb.set_trace()
                            

                        warped_rect = CompColor(size=(pix_w, pix_h), label=label)
                        img = warped_rect.draw()
                        # self.image.paste(img,    (w*pix, h*pix))
                        self.og_image.paste(img, (w*pix, h*pix))

                        # if h%10 == 0:
                        #     import pdb; pdb.set_trace()
                        #     self.og_image.show()

                        self.occupy(w,h,pix_w/pix,pix_h/pix)

            # if w%38 == 0:
            #     self.og_image.show()
            #     import pdb; pdb.set_trace()



        self.og_image.show()
