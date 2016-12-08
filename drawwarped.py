

import util 

from PIL import Image, ImageDraw
from warped import Warped

class DrawWarped():

    def __init__(self, imgpath):
        self.og_image = Image.open(imgpath)
        self.image = Image.new('RGB', self.og_image.size)
        self.draw = ImageDraw.Draw(self.image, 'RGBA')


    def warp(self):
        width,height = self.image.size

        print width,height
        pix = 48

        for w in range(width/pix):
            for h in range(height/pix):

                x,y = w*pix,h*pix
                rect_coords = [x,y,x+pix, y+pix]

                color = util.average_color(self.og_image, rect=rect_coords)

                warped_rect = Warped(size=(pix,pix), color=color)
                img = warped_rect.draw()


                # self.draw.rectangle(shape.coords(), fill=color)
                self.image.paste(img, (w*pix,h*pix))
                # self.image.show()
                self.og_image.paste(img, (w*pix,h*pix))

                # self.og_image.show()
                # import pdb; pdb.set_trace()
                print w,h

            # self.og_image.show()
            # import pdb; pdb.set_trace()


        self.og_image.show()
