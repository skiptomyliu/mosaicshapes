

import util 

from PIL import Image, ImageDraw
from warped import Warped
from skimage.color import rgb2grey
from skimage import io, feature
import matplotlib.pyplot as plt
import numpy as np
from enum import Enum

class Slope(Enum):
    uphill = 1
    downhill = 2
    horizontal = 3
    vertical = 4
    

class DrawWarped():

    def __init__(self, imgpath):
        self.og_image = Image.open(imgpath)
        self.image = Image.new('RGB', self.og_image.size)
        self.draw = ImageDraw.Draw(self.image, 'RGBA')

        grey_img = rgb2grey(io.imread(imgpath))
        self.img_edges = feature.canny(grey_img, sigma=3)

        # plt.imshow(self.img_edges, cmap=plt.cm.gray)
        # plt.show()

    def get_slope(self, img_seg):
        # if len(img_seg[img_seg==True]) > len(img_seg[img_seg==False])/50:
        if len(img_seg[img_seg==True]):
            x,y = np.where(img_seg==True)

            slope,_ = np.polyfit(x,y,1)
            return slope

            if slope >= 0:
                return Slope.downhill
            elif slope < 0:
                return Slope.uphill
            # else:
            #     return Slope.horizontal



    def warp(self):
        width,height = self.image.size

        print width,height
        pix = 35

        # import pdb; pdb.set_trace()

        for w in range(width/pix):
            for h in range(height/pix):

                # create rect coords:
                x,y = w*pix,h*pix
                rect_coords = [x,y,x+pix, y+pix]

                slope = self.get_slope(self.img_edges[y:y+pix,x:x+pix])

                color = util.average_color(self.og_image, rect=rect_coords)
                if slope and not np.isnan(slope):
                    print [x,y,x+pix, y+pix]
                    if slope < 0: # uphill
                        color = (200,0,0)
                    if slope >= 0: # downhill
                        color = (0,255,0)
                    # import pdb; pdb.set_trace()
                    warped_rect = Warped(size=(pix,pix), color=color)
                    img = warped_rect.draw(slope)
                    self.image.paste(img, (w*pix,h*pix))
                    self.og_image.paste(img, (w*pix,h*pix))

                    # self.og_image.show()


                # warped_rect = Warped(size=(pix,pix), color=color)
                # img = warped_rect.draw()

                # # self.draw.rectangle(shape.coords(), fill=color)
                # self.image.paste(img, (w*pix,h*pix))
                # # self.image.show()
                # self.og_image.paste(img, (w*pix,h*pix))

                
                # print w,h

            # if w%10:
                # self.og_image.show()


        self.og_image.show()
