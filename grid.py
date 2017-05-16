
import util 
from PIL import Image, ImageFilter
from comp import CompColor
from trianglecell import TriangleCell
from circlecell import CircleCell
from rectcell import RectCell
from pieslicecell import PieSliceCell
from halfcirclecell import HalfCircleCell
from skimage.color import rgb2grey
from skimage import feature
import numpy as np
from numpy.random import randint
from colorpalette import ColorPalette
import random 
import imghdr
from gencolor import GenColor
import math

"""

- diamond grid instead of square grid
- multi-color cells 
- pieslice bottom needs to be moved up a little



x pixelwidth (pw) to use needs to be automated dependent on image size and n, sn count 
x - circle stretching needs to be fixed on 2x1 cells
x Need to supersample drawing triangles ... needs anti alias
x triangle drawing on 2x2 bleeds over
x - 2x1 rectcell is not centered
"""


class Grid():
    def __init__(self, imgpath, pix=0, pix_multi=-1, diamond=True, colorful=True, unsharp_radius=2, 
        working_res=0, enlarge=0):

        self.N = 2
        self.is_diamond = diamond
        self.is_colorful = int(colorful)

        self.imgpath = imgpath
        self.og_image = util.image_transpose_exif(Image.open(imgpath))
        self.width, self.height = self.og_image.size


        """
        """
        # multi = util.get_multi(self.og_image, enlarge)
        # self.og_size2 = self.og_image.size[0]*multi, self.og_image.size[1]*multi
        # print multi
        # rotated_img = self.og_image.rotate(45, expand=True)

        # rotated_size = self.og_size2[0], self.og_size2[1]
        # # target_length = int(self.og_size2[0]*math.cos(45*math.pi/180) + self.og_size2[1]*math.sin(45*math.pi/180))+1
        # target_length = int(self.og_size2[0]*math.cos(45*math.pi/180) + self.og_size2[1]*math.sin(45*math.pi/180))+1
        # rotated_og = rotated_img.rotate(-45)

        """
        """
        if enlarge > 0:
            self.enlarge = enlarge
        else:
            self.enlarge = max(self.og_image.size[0], self.og_image.size[1])

        # Convert to JPEG if png
        if imghdr.what(imgpath) == 'png':
            self.og_image = util.png_to_jpeg(self.og_image)

        # If our enlarge is less than the resolution of our input, we set working res
        #  as the enlarge
        if self.enlarge < max(self.og_image.size[0], self.og_image.size[1]):
            working_res = self.enlarge

        if working_res:
            # print "*"*10
            # print "working res"
            # print "*"*10
            # print self.og_image
            if working_res < self.og_image.size[0] and working_res < self.og_image.size[1]:
                self.og_image = util.restrain_img_size(self.og_image, max_pix=working_res)                
            else:
                self.og_image = util.enlarge_img(self.og_image, max_pix=working_res)


        self.N = util.get_multi(self.og_image, self.enlarge*2)

        multi = util.get_multi(self.og_image, self.enlarge)
        t_size = multi*self.og_image.size[0], multi*self.og_image.size[1]
        self.target_size = t_size
        # self.target_length = int(t_size[0]*math.cos(45*math.pi/180) + t_size[1]*math.sin(45*math.pi/180))+1

        if self.is_diamond:
            self.og_size = self.og_image.size[0]*self.N, self.og_image.size[1]*self.N #self.canvas_img.size
            self.og_image = self.og_image.rotate(45, expand=True, resample=Image.BICUBIC)
            # XXX:  Use this one if we don't care about showing updates
            # self.canvas_img = Image.new('RGBA', (self.og_image.size[0]*self.N, self.og_image.size[1]*self.N))
            # self.canvas_img = util.mult_img_size(self.og_image, self.N)
            # self.canvas_img = self.canvas_img.rotate(45, expand=True, resample=Image.BICUBIC)
        else:
            self.og_size = self.width, self.height


        self.canvas_img = util.mult_img_size(self.og_image, self.N)
        self.edg_img = self.og_image.filter(ImageFilter.UnsharpMask(2, percent=300))
        self.image_array = np.array(self.edg_img)
        # Find edges
        self.img_edges = feature.canny(rgb2grey(self.image_array), sigma=2) #, low_threshold=10, high_threshold=20)
        self.width,self.height = self.og_image.size


        # Determine our grid size:
        longest = self.width if self.width>self.height else self.height
        if pix_multi > 0 and pix_multi < 1:
            self.pixels = int(round(longest*pix_multi))
        elif pix > 0:
            self.pixels = int(pix)
        else:
            self.pixels = int(longest*.013)

        self.cols = (self.width/self.pixels)
        self.rows = (self.height/self.pixels)

        # print self.og_image.size
        # print "N: " + str(self.N)
        # print "multi: " + str(multi)
        # print self.pixels, self.cols, self.rows
        # import pdb; pdb.set_trace()

        # Crop the image if our pixels doesn't divide equally.  Most cases we always crop
        # will prevent out of bounds processing on cells
        #XXX Does this work for diamonds too?
        self.og_image = self.og_image.crop((0, 0, self.cols*self.pixels, self.rows*self.pixels))
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

        base_colors_4 = GenColor.gen_colors(base_color, 4, self.is_colorful)
        base_colors_3 = GenColor.gen_colors(base_color, 3, self.is_colorful)
        base_colors_2 = GenColor.gen_colors(base_color, 2, self.is_colorful)
    
        # second_colors_3 = GenColor.gen_colors(second_color, 3, self.is_colorful)        
        second_colors_2 = GenColor.gen_colors(second_color, 2, self.is_colorful)

        
        circle,circle_rms = CircleCell.find_best(cropped_img, base_colors=base_colors_3, second_colors=second_colors_2, N=self.N)
        rect,rect_rms = RectCell.find_best(cropped_img, base_colors=base_colors_2, second_colors=second_colors_2, N=self.N)
        pie,pie_rms = PieSliceCell.find_best(cropped_img, base_colors=base_colors_3, second_colors=second_colors_2, N=self.N)
        halfc,halfc_rms = HalfCircleCell.find_best(cropped_img, base_colors=base_colors_3, second_colors=second_colors_2, N=self.N)
        triangle,triangle_rms = TriangleCell.find_best(cropped_img, base_colors=base_colors_4, second_colors=second_colors_2, N=self.N)

        # missing triangles
        # circle,circle_rms = CircleCell.find_best(cropped_img, n=3, sn=2, base_color=base_color, second_color=second_color, colorful=self.is_colorful, N=self.N)
        # rect,rect_rms = RectCell.find_best(cropped_img, n=2, sn=2, base_color=base_color, second_color=second_color, colorful=self.is_colorful, N=self.N)
        # pie,pie_rms = PieSliceCell.find_best(cropped_img, n=3, sn=2, base_color=base_color, second_color=second_color, colorful=self.is_colorful, N=self.N)
        # halfc,halfc_rms = HalfCircleCell.find_best(cropped_img, n=3, sn=2, base_color=base_color, second_color=second_color, colorful=self.is_colorful, N=self.N)
        # triangle commented out missing

        # Order matters!  shape and rms list must match same order
        shapes = [circle, rect, pie, halfc, triangle]
        rms_list = [circle_rms, rect_rms, pie_rms, halfc_rms, triangle_rms]

        shape = shapes[rms_list.index(min(rms_list))]

        return shape

    # XXX: rename n_pass
    def n_pass(self, n_total=-1):
        self.grid_start_end(0, self.rows)

    def grid_start_end_thread(self, (s_row, f_row, out_path)):
        self.grid_start_end(s_row, f_row)
        self.save(out_path)
        # print "{s},{e}".format(s=s_row, e=f_row)

    def grid_start_end(self, s_row, f_row):
        width,height = self.og_image.size
        pix = self.pixels

        for row in range(self.rows)[s_row:f_row]:
            for col in range(self.cols):
                if not self.is_occupied(col,row):
                    pix_w, pix_h = (pix, pix)

                    # create rect coords:
                    # if randint(0,50)==1:
                    #     pix_w, pix_h = (pix*2, pix*1)
                    # elif randint(0,50)==1:
                    #     pix_w, pix_h = (pix, pix*2)
                    # else:
                    #     pix_w, pix_h = (pix, pix)

                    x,y = col*pix, row*pix
                    rect_coords = [
                        x, y, 
                        util.clamp_int(x+pix_w, 0, width), util.clamp_int(y+pix_h, 0, height)
                    ]
                    edges_seg = self.img_edges[y:y+pix_w,x:x+pix_h]

                    # If pixel has edge:
                    if np.any(edges_seg) and len(np.where(edges_seg)[1]):
                        cropped_img = self.og_image.crop(rect_coords)

                        # First find doubles
                        rect_coords2 = rect_coords[:]

                        if randint(0,2): # 0 or 1
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

                        if rms_v < 40:
                            rect_coords3 = [rect_coords[0], rect_coords[1], rect_coords2[2], rect_coords2[3]]
                            big_crop_img = self.og_image.crop(rect_coords3)
                            # shape = self.best_shape(big_crop_img)
                            # img = shape.draw()
                            img = self.best_shape(big_crop_img)
                            
                        else:
                            # shape = self.best_shape(cropped_img)
                            # img = shape.draw()
                            img = self.best_shape(cropped_img)
                            pix_w,pix_h=pix,pix

                    else:
                        og_color = util.average_color_img(self.og_image.crop(rect_coords))
                        base_colors = GenColor.gen_colors(og_color, randint(3,5), self.is_colorful)
                        ccolor = CompColor(size=(pix_w, pix_h), base_colors=base_colors)
                        # ccolor = CompColor(size=(pix_w, pix_h), base_color=og_color, n=4, colorful=self.is_colorful)
                        img = ccolor.draw(self.N)

                    self.canvas_img.paste(img, (int(x*self.N),int(y*self.N)))
                    self.occupy(col,row,pix_w/pix,pix_h/pix)

        # self.canvas_img.show()



    def crop_grid(self, img, N=2):
        return img.crop((0, 0, self.cols*self.pixels*N, self.rows*self.pixels*N))

    def restore_diamond(self):

        # target_length = int(self.og_size2[0]*math.cos(45*math.pi/180) + self.og_size2[1]*math.sin(45*math.pi/180))+1

        diamond_img = self.canvas_img.rotate(-45, expand=False, resample=Image.BICUBIC)
        return diamond_img.crop((
            (self.canvas_img.size[0] - self.og_size[0])/2,
            (self.canvas_img.size[1] - self.og_size[1])/2,
            self.og_size[0] + (self.canvas_img.size[0] - self.og_size[0])/2,
            self.og_size[1] + (self.canvas_img.size[1] - self.og_size[1])/2,
            ))

    def save(self, path, dpi=300, is_continue=False):
        if self.is_diamond:
            # resize_scale = self.canvas_img.size[1]/float(self.target_length)
            # diamond_img = util.mult_img_size(self.canvas_img, 1/resize_scale)
            diamond_img = util.mult_img_size(self.canvas_img.copy(), .5)
            diamond_img = diamond_img.rotate(-45, expand=False, resample=Image.BICUBIC)

            diamond_img = diamond_img.crop((
                (diamond_img.size[0] - self.target_size[0])/2 + self.pixels,
                (diamond_img.size[1] - self.target_size[1])/2 + self.pixels,
                self.target_size[0] + (diamond_img.size[0] - self.target_size[0])/2 - self.pixels,
                self.target_size[1] + (diamond_img.size[1] - self.target_size[1])/2 - self.pixels,
            ))
            diamond_img.save(path, "jpeg", icc_profile=self.og_image.info.get('icc_profile'), quality=95, dpi=(dpi,dpi))    
        else:
            grid_img = self.canvas_img.copy()
            if not is_continue:
                grid_img = self.crop_grid(grid_img, self.N)
            grid_img = util.restrain_img_size(grid_img, self.enlarge)
            grid_img.save(path, "jpeg", icc_profile=self.og_image.info.get('icc_profile'), quality=95, dpi=(dpi,dpi))

