
import util 
from PIL import Image, ImageDraw
from warped import Warped
from comp import CompColor
from trianglecell import TriangleCell
from circlecell import CircleCell
from rectcell import RectCell
from pieslicecell import PieSliceCell
from halfcirclecell import HalfCircleCell
from skimage.color import rgb2grey
from skimage import io, feature
import numpy as np
from enum import Enum
from colorpalette import ColorPalette
import random 
import os
import imghdr
import functools

"""
- find best quantize image, refactor so quantize once 

- diamond grid instead of square grid
- multi-color cells 
- pieslice bottom needs to be moved up a little
- shrink edge cells
- experiment with quantize og_image prior to gridding 



x pixelwidth (pw) to use needs to be automated dependent on image size and n, sn count 
x - circle stretching needs to be fixed on 2x1 cells
x Need to supersample drawing triangles ... needs anti alias
x triangle drawing on 2x2 bleeds over
x - 2x1 rectcell is not centered
"""
class Grid():
    def __init__(self, imgpath, pix=0, restrain=False):
        self.imgpath = imgpath
        self.og_image = util.image_transpose_exif(Image.open(imgpath))
        if restrain:
            self.og_image = util.restrain_img_size(self.og_image)
        print(self.og_image.size)
	   
        if imghdr.what(imgpath) == 'png':
            self.og_image = util.png_to_jpeg(self.og_image)

        self.image = Image.new('RGB', self.og_image.size)
        self.draw = ImageDraw.Draw(self.image, 'RGBA')
        self.image_array = np.array(self.og_image)
        self.img_edges = feature.canny(rgb2grey(self.image_array), sigma=4)

        self.width,self.height = self.image.size
        longest = self.width if self.width>self.height else self.height
        self.pixels = pix if pix>0 else int(round(longest*.018))
        print self.pixels

        self.cols = (self.width/self.pixels)
        self.rows = (self.height/self.pixels)
        self.grid_status = np.zeros([self.width/self.pixels, self.height/self.pixels])

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

    def best_shape(self, cropped_img):
        second_color,base_color = ColorPalette.quantize_img(cropped_img, 2)

        circle = CircleCell.find_best(cropped_img, n=3, sn=2, base_color=base_color, second_color=second_color)
        rect = RectCell.find_best(cropped_img, n=2, sn=2, base_color=base_color, second_color=second_color)
        triangle = TriangleCell.find_best(cropped_img, n=2, sn=1, base_color=base_color, second_color=second_color)
        pie = PieSliceCell.find_best(cropped_img, n=3, sn=2, base_color=base_color, second_color=second_color)
        halfc = HalfCircleCell.find_best(cropped_img, n=3, sn=2, base_color=base_color, second_color=second_color)

        circle_rms = util.rmsdiff(cropped_img, circle.draw())
        rect_rms = util.rmsdiff(cropped_img, rect.draw())
        triangle_rms = util.rmsdiff(cropped_img, triangle.draw())
        pie_rms = util.rmsdiff(cropped_img, pie.draw())
        halfc_rms = util.rmsdiff(cropped_img, halfc.draw())
        
        shapes = [circle, rect, triangle, pie, halfc]
        rms_list = [circle_rms, rect_rms, triangle_rms, pie_rms, halfc_rms]
        shape = shapes[rms_list.index(min(rms_list))]

        return shape

    # XXX: rename n_pass
    def n_pass(self, n_total=-1):
        self.grid_start_end(0, self.rows)

    def grid_start_end(self, s_row, f_row):
        width,height = self.image.size
        pix = self.pixels

        for row in range(self.rows)[s_row:f_row]:
            for col in range(self.cols):
                if not self.is_occupied(col,row):
                    pix_w, pix_h = (pix, pix)

                    # create rect coords:
                    # if random.randint(0,50)==1:
                    #     pix_w, pix_h = (pix*2, pix*1)
                    # elif random.randint(0,50)==1:
                    #     pix_w, pix_h = (pix, pix*2)
                    # else:
                    #     pix_w, pix_h = (pix, pix)

                    x,y = col*pix, row*pix
                    rect_coords = [
                        x, y, 
                        util.clamp_int(x+pix_w, 0, width), util.clamp_int(y+pix_h, 0, height)
                    ]
                    edges_seg = self.img_edges[y:y+pix_w,x:x+pix_h]
                    if np.any(edges_seg) and len(np.where(edges_seg)[1]):
                        cropped_img = self.og_image.crop(rect_coords)

                        # First find doubles
                        rect_coords2 = rect_coords[:]
                        if random.randint(0,1):
                            """
                            vertical 
                            """
                            rect_coords2[1] = rect_coords2[1] + pix
                            rect_coords2[3] = util.clamp_int(rect_coords2[3] + pix, 0, height)
                            pix_h*=2
                        else:
                            """
                            horizontal 
                            """
                            rect_coords2[0] = rect_coords2[0] + pix
                            rect_coords2[2] = util.clamp_int(rect_coords2[2] + pix, 0, width)
                            pix_w*=2
                        cropped_img2 = self.og_image.crop(rect_coords2)
                        rms_v = util.rmsdiff(cropped_img, cropped_img2)

                        if rms_v < 70:
                            rect_coords3 = [rect_coords[0], rect_coords[1], rect_coords2[2], rect_coords2[3]]
                            big_crop_img = self.og_image.crop(rect_coords3)
                            shape = self.best_shape(big_crop_img)
                            img = shape.draw()
                        else:
                            shape = self.best_shape(cropped_img)

                            if isinstance(shape, TriangleCell):
                                area = edges_seg.shape[0]*edges_seg.shape[1]
                                percent = (len(np.where(edges_seg)[1])*2)/float(area)
                                # if percent <= .2:
                                #     shape.shrink = 4
                                # if percent <= .1:
                                #     shape.shrink = 6

                            img = shape.draw()
                            pix_w,pix_h=pix,pix

                    else:
                        og_color = util.average_color_img(self.og_image.crop(rect_coords))
                        ccolor = CompColor(size=(pix_w, pix_h), base_color=og_color, n=4)
                        img = ccolor.draw()

                    self.og_image.paste(img, (x,y))
                    self.occupy(col,row,pix_w/pix,pix_h/pix)

    # def n_pass(self, n_total=-1):

    #     width,height = self.image.size
    #     pix = self.pixels

    #     for row in range(self.rows):
    #         for col in range(self.cols):
    #             if not self.is_occupied(col,row):
    #                 pix_w, pix_h = (pix, pix)

    #                 # create rect coords:
    #                 # if random.randint(0,50)==1:
    #                 #     pix_w, pix_h = (pix*2, pix*1)
    #                 # elif random.randint(0,50)==1:
    #                 #     pix_w, pix_h = (pix, pix*2)
    #                 # else:
    #                 #     pix_w, pix_h = (pix, pix)

    #                 x,y = col*pix, row*pix
    #                 rect_coords = [
    #                     x, y, 
    #                     util.clamp_int(x+pix_w, 0, width), util.clamp_int(y+pix_h, 0, height)
    #                 ]
    #                 edges_seg = self.img_edges[y:y+pix_w,x:x+pix_h]
    #                 if np.any(edges_seg) and len(np.where(edges_seg)[1]):
    #                     cropped_img = self.og_image.crop(rect_coords)

    #                     # First find doubles
    #                     rect_coords2 = rect_coords[:]
    #                     if random.randint(0,1):
    #                         """
    #                         vertical 
    #                         """
    #                         rect_coords2[1] = rect_coords2[1] + pix
    #                         rect_coords2[3] = util.clamp_int(rect_coords2[3] + pix, 0, height)
    #                         pix_h*=2
    #                     else:
    #                         """
    #                         horizontal 
    #                         """
    #                         rect_coords2[0] = rect_coords2[0] + pix
    #                         rect_coords2[2] = util.clamp_int(rect_coords2[2] + pix, 0, width)
    #                         pix_w*=2
    #                     cropped_img2 = self.og_image.crop(rect_coords2)
    #                     rms_v = util.rmsdiff(cropped_img, cropped_img2)

    #                     if rms_v < 70:
    #                         rect_coords3 = [rect_coords[0], rect_coords[1], rect_coords2[2], rect_coords2[3]]
    #                         big_crop_img = self.og_image.crop(rect_coords3)
    #                         shape = self.best_shape(big_crop_img)
    #                         img = shape.draw()
    #                     else:
    #                         shape = self.best_shape(cropped_img)

    #                         if isinstance(shape, TriangleCell):
    #                             area = edges_seg.shape[0]*edges_seg.shape[1]
    #                             percent = (len(np.where(edges_seg)[1])*2)/float(area)
    #                             # if percent <= .2:
    #                             #     shape.shrink = 4
    #                             # if percent <= .1:
    #                             #     shape.shrink = 6

    #                         img = shape.draw()
    #                         pix_w,pix_h=pix,pix

    #                 else:
    #                     og_color = util.average_color_img(self.og_image.crop(rect_coords))
    #                     ccolor = CompColor(size=(pix_w, pix_h), base_color=og_color, n=4)
    #                     img = ccolor.draw()

    #                 self.og_image.paste(img, (x,y))
    #                 self.occupy(col,row,pix_w/pix,pix_h/pix)

    #     #self.og_image.show()
    #     self.og_image.save("out.JPEG", "jpeg", icc_profile=self.og_image.info.get('icc_profile'), quality=95, dpi=(200,200))
        

    def save(self, path):
        filename=os.path.basename(self.imgpath)
        out_path = "{path}/{fname}_abs.JPEG".format(path=path, fname=filename)
        print("output: " + out_path)
        self.og_image.save(out_path, "jpeg", icc_profile=self.og_image.info.get('icc_profile'), quality=95, dpi=(200,200))

