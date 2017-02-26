

import util
from circlecell import CircleCell
from PIL import Image, ImageDraw

class Dottify():

    def __init__(self, imgpath):

        self.og_image = util.image_transpose_exif(Image.open(imgpath))
        self.width, self.height = self.og_image.size

        self.pixels = 25
        self.cols = (self.width/self.pixels)
        self.rows = (self.height/self.pixels)



    def paint(self):
        pix = self.pixels


        # self.og_image.quantize(colors=2).convert('RGB').show()

        paper = Image.new('RGBA', (self.width, self.height), (0,255,255,255))
        canvas = ImageDraw.Draw(paper)


        mask = Image.new(size=(pix, pix), mode='RGBA', color=(200,0,0,0))
        
        for row in range(self.rows):
            for col in range(self.cols):
                x,y = col*pix, row*pix

                rect_coords = [
                    x, y, 
                    util.clamp_int(x+pix, 0, self.width), util.clamp_int(y+pix, 0, self.height)
                ]
                cropped_img = self.og_image.crop(rect_coords)

                r,g,b = util.average_color_img(cropped_img)

                cpix = util.luminance(r,g,b)

                circle = self.ellipse((pix,pix),(cpix,cpix),(0,255,0,255))
                paper.paste(circle, (x,y), mask=circle)
                
            # paper.show()

        paper.show()
        # self.og_image.show()



    def ellipse(self, size, csize, color):
        w,h = size
        cw,ch = csize
        circle_paper = Image.new('RGBA', size, (0,0,0,0))
        circle_canvas = ImageDraw.Draw(circle_paper)

        sx = (w-cw)
        sy = (h-ch)

        circle_canvas.ellipse((sx, sy, sx+cw, sy+ch), fill=(0,200,200,255))


        return circle_paper

    # def draw_ellipse(self, image, bounds, width=1, outline='white', antialias=4):
    #     """Improved ellipse drawing function, based on PIL.ImageDraw."""

    #     # Use a single channel image (mode='L') as mask.
    #     # The size of the mask can be increased relative to the imput image
    #     # to get smoother looking results. 
    #     mask = Image.new(
    #         size=[int(dim * antialias) for dim in image.size],
    #         mode='L', color='black')
    #     draw = ImageDraw.Draw(mask)

    #     # draw outer shape in white (color) and inner shape in black (transparent)
    #     for offset, fill in (width/-2.0, 'white'), (width/2.0, 'black'):
    #         left, top = [(value + offset) * antialias for value in bounds[:2]]
    #         right, bottom = [(value - offset) * antialias for value in bounds[2:]]
    #         draw.ellipse([left, top, right, bottom], fill=fill)

    #     # downsample the mask using PIL.Image.LANCZOS 
    #     # (a high-quality downsampling filter).
    #     mask = mask.resize(image.size, Image.LANCZOS)
    #     # paste outline color to input image through the mask
    #     image.paste(outline, mask=mask)

      

