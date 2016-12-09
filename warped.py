


from PIL import Image, ImageDraw
import numpy as np
# from numpy import random
import random
import matplotlib.pyplot as plt
from skimage.transform import PiecewiseAffineTransform, warp
import scipy
from scipy.misc import toimage
from random import shuffle

import util


"""
Get average color of rect.
Draw multiple circles inside each other.  
Distort it (http://stackoverflow.com/questions/21940911/python-image-distortion)
"""
class Warped():

    def __init__(self, size=(200,200), color=(180,0,200)):
        self.width = size[0]
        self.height = size[1]
        self.color = color
        self.num_circles = 4
        self.warp_height = .04*np.random.random()

        self.sincos = np.sin#np.cos if bool(random.getrandbits(1)) else np.sin

    def __paint_circles(self):
        pass


    # def draw(self):
    #     show_image = False

    #     is_horizontal = True if self.width >= self.height else False

    #     if is_horizontal:
    #         ratio = self.width / float(self.height)
    #     else:
    #         ratio = self.height / float(self.width)

    #     CIRCLE_SIZE = max(self.width, self.height)
        
    #     print "circle size", CIRCLE_SIZE

    #     circle_img = Image.new('RGBA', (CIRCLE_SIZE,CIRCLE_SIZE))

    #     canvas = ImageDraw.Draw(circle_img)

    #     csize = CIRCLE_SIZE/(self.num_circles*2)

    #     color0 = self.color #(100,100,200)
    #     color1, color2 = util.adjacent_colors(color0)
    #     color3, color4 = util.adjacent_colors(color1)
    #     color4, color5 = util.adjacent_colors(color2)
    #     colors = [color0, color1, color2, color3, color4, color5]

    #     shuffle(colors)
    #     # print colors

    #     paper = Image.new('RGBA', (CIRCLE_SIZE,CIRCLE_SIZE))
    #     paper.paste(colors[0], [0,0,self.width,self.height])

    #     canvas.ellipse([0, 0, CIRCLE_SIZE,CIRCLE_SIZE], fill=colors[1])
    #     canvas.ellipse([csize, csize, CIRCLE_SIZE-csize, CIRCLE_SIZE-csize], fill=colors[2])
    #     canvas.ellipse([csize*2, csize*2, CIRCLE_SIZE-csize*2, CIRCLE_SIZE-csize*2], fill=colors[3])
    #     canvas.ellipse([csize*3, csize*3, CIRCLE_SIZE-csize*3, CIRCLE_SIZE-csize*3], fill=colors[4])

    #     # paper = Image.new('RGBA', (CIRCLE_SIZE,CIRCLE_SIZE))
    #     # paper.paste(color0, [0,0,self.width,self.height])
    #     # canvas.ellipse([0, 0, CIRCLE_SIZE,CIRCLE_SIZE], fill=color1)
    #     # canvas.ellipse([csize, csize, CIRCLE_SIZE-csize, CIRCLE_SIZE-csize], fill=color2)
    #     # canvas.ellipse([csize*2, csize*2, CIRCLE_SIZE-csize*2, CIRCLE_SIZE-csize*2], fill=color3)
    #     # canvas.ellipse([csize*3, csize*3, CIRCLE_SIZE-csize*3, CIRCLE_SIZE-csize*3], fill=color4)


    #     if show_image:
    #         circle_img.show()
    #     image = np.asarray(circle_img)
    #     # rows, cols = image.shape[0], image.shape[1]
    #     rows, cols = self.height, self.width

    #     src_cols = np.linspace(0, cols, 50)
    #     src_rows = np.linspace(0, rows, 50)
    #     src_rows, src_cols = np.meshgrid(src_rows, src_cols)
    #     src = np.dstack([src_cols.flat, src_rows.flat])[0]

    #     # add sinusoidal oscillation to row coordinates
    #     HEIGHT_OSC = CIRCLE_SIZE * self.warp_height

    #     if is_horizontal:
    #         dst_rows = src[:, 1] - self.sincos(np.linspace(0, 4 * np.pi, src.shape[0])) * HEIGHT_OSC
    #         dst_cols = src[:, 0] 

    #         dst_rows *= (ratio+self.warp_height)
    #         dst_rows -= ratio * HEIGHT_OSC # subtract y position to account for mutating up
    #     else:
    #         dst_rows = src[:, 1] 
    #         dst_cols = src[:, 0]  - self.sincos(np.linspace(0, 3 * np.pi, src.shape[0])) * HEIGHT_OSC

    #         dst_cols *= (ratio+self.warp_height)
    #         # dst_cols -= ratio * HEIGHT_OSC # subtract y position to account for mutating up

    #     dst = np.vstack([dst_cols, dst_rows]).T

    #     tform = PiecewiseAffineTransform()
    #     tform.estimate(src, dst)

    #     out_rows = rows #image.shape[0] - 1.5 * HEIGHT_OSC
    #     out_cols = cols

    #     print out_cols, out_rows
    #     out = warp(image, tform, output_shape=(out_rows, out_cols))

    #     # fig, ax = plt.subplots()


    #     # if show_image:
    #     #     ax.imshow(out)
    #     #     # ax.plot(tform.inverse(src)[:, 0], tform.inverse(src)[:, 1], '.b') # plots the dots
    #     #     ax.axis((0, out_cols, out_rows, 0))
    #     #     plt.show()

    #     converted = scipy.misc.toimage(out)

    #     # import pdb; pdb.set_trace()
    #     # paper.paste(converted, (0,0))
    #     paper.paste(converted, (0, 0), converted)
    #     # if show_image:
    #     #     converted.show()

    #     return paper



    def draw(self, slope=1):
        show_image = False

        is_horizontal = True if self.width >= self.height else False

        if is_horizontal:
            ratio = self.width / float(self.height)
        else:
            ratio = self.height / float(self.width)

        CIRCLE_SIZE = max(self.width, self.height)
        
        print "circle size", CIRCLE_SIZE

        circle_img = Image.new('RGBA', (CIRCLE_SIZE,CIRCLE_SIZE))

        canvas = ImageDraw.Draw(circle_img)

        csize = CIRCLE_SIZE/(self.num_circles*2)

        color0 = self.color # (100,100,200)
        color1, color2 = util.adjacent_colors(color0)
        color3, color4 = util.adjacent_colors(color1)
        color4, color5 = util.adjacent_colors(color2)
        colors = [color0, color1, color2, color3, color4, color5]

        shuffle(colors)
        # print colors

        paper = Image.new('RGBA', (CIRCLE_SIZE,CIRCLE_SIZE))
        paper.paste(colors[0], [0,0,self.width,self.height])

        canvas.ellipse([0, 0, CIRCLE_SIZE,CIRCLE_SIZE], fill=colors[1])
        canvas.ellipse([csize, csize, CIRCLE_SIZE-csize, CIRCLE_SIZE-csize], fill=colors[2])
        canvas.ellipse([csize*2, csize*2, CIRCLE_SIZE-csize*2, CIRCLE_SIZE-csize*2], fill=colors[3])
        canvas.ellipse([csize*3, csize*3, CIRCLE_SIZE-csize*3, CIRCLE_SIZE-csize*3], fill=colors[4])

        # paper = Image.new('RGBA', (CIRCLE_SIZE,CIRCLE_SIZE))
        # paper.paste(color0, [0,0,self.width,self.height])
        # canvas.ellipse([0, 0, CIRCLE_SIZE,CIRCLE_SIZE], fill=color1)
        # canvas.ellipse([csize, csize, CIRCLE_SIZE-csize, CIRCLE_SIZE-csize], fill=color2)
        # canvas.ellipse([csize*2, csize*2, CIRCLE_SIZE-csize*2, CIRCLE_SIZE-csize*2], fill=color3)
        # canvas.ellipse([csize*3, csize*3, CIRCLE_SIZE-csize*3, CIRCLE_SIZE-csize*3], fill=color4)

        # if show_image:
        #     circle_img.show()
        image = np.asarray(circle_img)
        # rows, cols = image.shape[0], image.shape[1]
        rows, cols = self.height, self.width

        src_cols = np.linspace(0, cols, 50)
        src_rows = np.linspace(0, rows, 50)
        src_rows, src_cols = np.meshgrid(src_rows, src_cols)
        src = np.dstack([src_cols.flat, src_rows.flat])[0]

        # add sinusoidal oscillation to row coordinates
        HEIGHT_OSC = CIRCLE_SIZE * self.warp_height

        if is_horizontal:
            dst_rows = src[:, 1] - self.sincos(np.linspace(0, .9 * np.pi, src.shape[0])) * HEIGHT_OSC
            dst_cols = src[:, 0] 

            dst_rows *= (ratio+self.warp_height+3)
            # dst_rows -=  800#* (ratio+self.warp_height)
            # dst_rows -= (ratio * HEIGHT_OSC) # subtract y position to account for mutating up
        else:
            dst_rows = src[:, 1] 
            dst_cols = src[:, 0]  - self.sincos(np.linspace(0, 3 * np.pi, src.shape[0])) * HEIGHT_OSC

            dst_cols *= (ratio+self.warp_height)
            # dst_cols -= ratio * HEIGHT_OSC # subtract y position to account for mutating up

        dst = np.vstack([dst_cols, dst_rows]).T

        tform = PiecewiseAffineTransform()
        tform.estimate(src, dst)

        out_rows = rows #image.shape[0] - 1.5 * HEIGHT_OSC
        out_cols = cols

        print out_cols, out_rows
        out = warp(image, tform, output_shape=(out_rows, out_cols))
        # import pdb; pdb.set_trace()

        slope_percent = 100*slope
        deg = np.degrees(np.arctan(-1*slope))
        out = scipy.ndimage.interpolation.rotate(out, deg)
        # out = scipy.ndimage.interpolation.rotate(out, 45)
        # out = scipy.ndimage.interpolation.rotate(out, 45)


        if show_image:
            fig, ax = plt.subplots()
            ax.imshow(out)
            # ax.plot(tform.inverse(src)[:, 0], tform.inverse(src)[:, 1], '.b') # plots the dots
            ax.axis((0, out_cols, out_rows, 0))
            plt.show()

        try:
            converted = scipy.misc.toimage(out)
        except Exception as e:
            import pdb; pdb.set_trace()

        # import pdb; pdb.set_trace()
        # paper.paste(converted, (0,0))
        paper.paste(converted, (0, 0), converted)
        if show_image:
            converted.show()
            # paper.show()

        return paper







