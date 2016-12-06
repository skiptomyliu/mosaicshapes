


import aggdraw


from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import PiecewiseAffineTransform, warp
import scipy
from scipy.misc import toimage

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
        self.num_circles = 3


    # def draw(self, canvas, color):
 #        print "rect"
 #        canvas.rectangle(self.coords(), fill=color)


    def draw(self):
        CIRCLE_SIZE = self.width
        circle_img=Image.new('RGB', (CIRCLE_SIZE,CIRCLE_SIZE))
        canvas = ImageDraw.Draw(circle_img)
        canvas.ellipse([0,0,CIRCLE_SIZE,CIRCLE_SIZE], fill=(240))
        canvas.ellipse([10,10,CIRCLE_SIZE-10,CIRCLE_SIZE-10], fill=(100,100,200))
        # circle_img.show()
        image = np.asarray(circle_img)
        rows, cols = image.shape[0], image.shape[1]

        # import pdb; pdb.set_trace()

        src_cols = np.linspace(0, cols, 20)
        src_rows = np.linspace(0, rows, 20)
        src_rows, src_cols = np.meshgrid(src_rows, src_cols)
        src = np.dstack([src_cols.flat, src_rows.flat])[0]

        # add sinusoidal oscillation to row coordinates
        HEIGHT_OSC = CIRCLE_SIZE*1/10
        dst_rows = src[:, 1] - np.sin(np.linspace(0, 3 * np.pi, src.shape[0])) * HEIGHT_OSC
        dst_cols = src[:, 0] #- np.sin(np.linspace(0, 3 * np.pi, src.shape[1])) * 50
        dst_rows *= 2.0
        dst_rows -= 2.0 * HEIGHT_OSC #subtract y position to account for mutating up
        dst = np.vstack([dst_cols, dst_rows]).T

        tform = PiecewiseAffineTransform()
        tform.estimate(src, dst)

        out_rows = image.shape[0] - 1.5 * HEIGHT_OSC
        out_cols = cols
        out = warp(image, tform, output_shape=(out_rows, out_cols))

        fig, ax = plt.subplots()
        ax.imshow(out)
        # ax.plot(tform.inverse(src)[:, 0], tform.inverse(src)[:, 1], '.b') # plots the dots
        ax.axis((0, out_cols, out_rows, 0))
        plt.show()

        converted = scipy.misc.toimage(out)
        converted.show()








