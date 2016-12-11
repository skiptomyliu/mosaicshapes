


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

todo:
draw outside square as complimentary? two squares total 
circle as the average primary in middle 



Get average color of rect.
Draw multiple circles inside each other.  
Distort it (http://stackoverflow.com/questions/21940911/python-image-distortion)
"""
class Warped():

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
        show_image = False
        draw_circle = False
        CIRCLE_SIZE = max(self.width, self.height)
        if draw_circle:
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

            color0 = self.fg_color # (100,100,200)

            r, g, b = self.fg_color
            r, g, b = [x/255.0 for x in r, g, b]
            h, l, s = colorsys.rgb_to_hls(r, g, b)     # RGB -> HLS
            s = s + .25
            r, g, b = colorsys.hls_to_rgb(h, l, s)
            # color0 = (int(r),int(g),int(b))
            color0 = r,g,b
            color0 = [int(x*255.0) for x in r, g, b]
            color0 = tuple(color0)
            print color0
            # import pdb; pdb.set_trace()

            color1, color2 = util.adjacent_colors(color0)
            color3, color4 = util.adjacent_colors(color1)
            color4, color5 = util.adjacent_colors(color2)
            colors = [color0, color1, color2, color3, color4, color5]

            shuffle(colors)
            # print colors

            canvas.ellipse([0, 0, CIRCLE_SIZE,CIRCLE_SIZE], fill=colors[1])
            canvas.ellipse([csize, csize, CIRCLE_SIZE-csize, CIRCLE_SIZE-csize], fill=colors[2])
            canvas.ellipse([csize*2, csize*2, CIRCLE_SIZE-csize*2, CIRCLE_SIZE-csize*2], fill=colors[3])
            canvas.ellipse([csize*3, csize*3, CIRCLE_SIZE-csize*3, CIRCLE_SIZE-csize*3], fill=colors[4])


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

                if slope:
                    dst_rows *= (ratio+self.warp_height+.5)
                else:
                    dst_rows *= (ratio+self.warp_height+.5)
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

            if slope > -10000:
                slope_percent = 100*slope
                deg = np.degrees(np.arctan(-1*slope))
                out = scipy.ndimage.interpolation.rotate(out, deg)


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

       
        paper = Image.new('RGBA', (CIRCLE_SIZE,CIRCLE_SIZE))

        # 1st color
         # Set up canvas where the circle will be pasted on
        r,g,b = self.fg_color
        c,m,y,k = util.rgb_to_cmyk(r,g,b)

        # _,m,y,k = 0,0,0,0
        # c,_,y,_ = 0,0,0,0
        # c,m,_,k = 0,0,0,0
        # c,m,y,_ = 0,0,0,0
        # _,_,y,k = 0,0,0,0
        # _,_,_,k = 0,0,0,0
        _,_,_,_ = 0,0,0,0

        # c*=1.5
        # m*=1.5
        # y*=1.5
        # k*=2.0
        # _,m,y,k = 0,0,0,0

        c+=10
        c*=1.5
        # k*=1.5

        r1,g1,b1 = util.cmyk_to_rgb(c,m,y,k)
            
        # 2nd color
        c,m,y,k = util.rgb_to_cmyk(r,g,b)
        # c,m,_,_ = 0,0,0,0
        

        # m+=2
        m*=1.5

        # k*=1.5
        r2,g2,b2 = util.cmyk_to_rgb(c,m,y,k)


        # 3rd color
        c,m,y,k = util.rgb_to_cmyk(r,g,b)
        # _,m,y,_ = 0,0,0,0
        y+=10
        y*=1.5
        # k*=1.5
        r3,g3,b3 = util.cmyk_to_rgb(c,m,y,k)


        # 4th color
        c,m,y,k = util.rgb_to_cmyk(r,g,b)
        # c,m,y,_ = 0,0,0,0
        k*=1.1
        r4,g4,b4 = util.cmyk_to_rgb(c,m,y,k)


        # M+C
        c,m,y,k = util.rgb_to_cmyk(r,g,b)
        c+=2
        c*=1.5
        # m+=2
        m*=1.5
        r5,g5,b5 = util.cmyk_to_rgb(c,m,y,k)


        # M+Y
        c,m,y,k = util.rgb_to_cmyk(r,g,b)
        y*=1.1
        # m+=2
        m*=1.1
        r6,g6,b6 = util.cmyk_to_rgb(c,m,y,k)

        width = random.randint(2,4)
        rand = random.randint(0,3)
        # import pdb; pdb.set_trace()

        # colors = [(r1,g1,b1),(r2,g2,b2),(r3,g3,b3),(r4,g4,b4)]
        # shuffle(colors)

        # for i in range(len(colors)):
        #     paper.paste(colors[i], [i*width,i*width,self.width-width*i,self.height-width*i])

        canvas = ImageDraw.Draw(paper)
        
        if rand == 0:
            paper.paste((r1,g1,b1), [0,0,self.width,self.height])
            # paper.paste((r2,g2,b2), [width,width,self.width-width,self.height-width])
            paper.paste((r5,g5,b5), [width,width,self.width-width,self.height-width])
            canvas.ellipse([width,width,self.width-width,self.height-width], fill=(r3,g3,b3))
            # paper.paste((r3,g3,b3), [width*2,width*2,self.width-width*2,self.height-width*2])
            paper.paste((r4,g4,b4), [width*2,width*2,self.width-width*2,self.height-width*2])
            paper.paste((r6,g6,b6), [width*3,width*3,self.width-width*3,self.height-width*3])
        elif rand == 1:
            # paper.paste((r2,g2,b2), [0,0,self.width,self.height])
            paper.paste((r5,g5,b5), [0,0,self.width,self.height])
            paper.paste((r1,g1,b1), [width,width,self.width-width,self.height-width])

            canvas.ellipse([width,width,self.width-width,self.height-width], fill=(r3,g3,b3))
            canvas.ellipse([width*2,width*2,self.width-width*2,self.height-width*2], fill=(r6,g6,b6))
            # paper.paste((r3,g3,b3), [width*2,width*2,self.width-width*2,self.height-width*2])
            # paper.paste((r6,g6,b6), [width*3,width*3,self.width-width*3,self.height-width*3])
            paper.paste((r4,g4,b4), [width*3,width*3,self.width-width*3,self.height-width*3])
        elif rand == 2:
            paper.paste((r4,g4,b4), [0,0,self.width,self.height])
            # paper.paste((r2,g2,b2), [width,width,self.width-width,self.height-width])
            paper.paste((r6,g6,b6), [width,width,self.width-width,self.height-width])

            canvas.ellipse([width,width,self.width-width,self.height-width], fill=(r5,g5,b5))
            canvas.ellipse([width*2,width*2,self.width-width*2,self.height-width*2], fill=(r3,g3,b3))

            # paper.paste((r5,g5,b5), [width*2,width*2,self.width-width*2,self.height-width*2])
            # paper.paste((r3,g3,b3), [width*3,width*3,self.width-width*3,self.height-width*3])
            paper.paste((r1,g1,b1), [width*4,width*4,self.width-width*4,self.height-width*4])
        elif rand == 3:
            paper.paste((r6,g6,b6), [0,0,self.width,self.height])
            paper.paste((r4,g4,b4), [width,width,self.width-width,self.height-width])
            # paper.paste((r3,g3,b3), [width*2,width*2,self.width-width*2,self.height-width*2])
            # paper.paste((r2,g2,b2), [width*2,width*2,self.width-width*2,self.height-width*2])
            # paper.paste((r5,g5,b5), [width*3,width*3,self.width-width*3,self.height-width*3])
            canvas.ellipse([width,width,self.width-width,self.height-width], fill=(r3,g3,b3))
            canvas.ellipse([width*2,width*2,self.width-width*2,self.height-width*2], fill=(r5,g5,b5))
            paper.paste((r1,g1,b1), [width*3,width*3,self.width-width*3,self.height-width*3])
        elif rand == 4:
            paper.paste((r3,g3,b3), [0,0,self.width,self.height])
            # paper.paste((r2,g2,b2), [width,width,self.width-width,self.height-width])
            paper.paste((r6,g6,b6), [width,width,self.width-width,self.height-width])
            paper.paste((r5,g5,b5), [width*2,width*2,self.width-width*2,self.height-width*2])
            paper.paste((r4,g4,b4), [width*3,width*3,self.width-width*3,self.height-width*3])
            paper.paste((r1,g1,b1), [width*4,width*4,self.width-width*4,self.height-width*4])


        # paper.paste(converted, (0, 0), converted)
        if show_image:
            converted.show()

        return paper







