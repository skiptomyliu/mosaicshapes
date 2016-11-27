from PIL import Image, ImageDraw, ImageChops
import random
import math


class DrawShape():

    def __init__(self, imgpath):
        self.og_image = Image.open(imgpath)
        self.image = Image.new('RGB', self.og_image.size)
        self.draw = ImageDraw.Draw(self.image, 'RGBA')

        self.max_size = 1000
        self.min_size = 1000
        self.sub_max_by = 10
        self.alpha = 1000

    @staticmethod
    def add_tuple(p0, p1):
        return tuple(sum(x) for x in zip(p0, p1))

    @staticmethod
    def rect_area(rect):
        pos0 = rect[0]
        pos1 = rect[1]
        w = abs(pos0[0] - pos1[0])
        h = abs(pos0[1] - pos1[1])
        return w*h

    @staticmethod
    def rmsdiff(im1, im2):
        diff = ImageChops.difference(im1, im2)
        h = diff.histogram()
        sq = (value*((idx%256)**2) for idx, value in enumerate(h))
        sum_of_squares = sum(sq)
        rms = math.sqrt(sum_of_squares/float(im1.size[0] * im1.size[1]))
        return rms

    def random_pos(self):
        w,h = self.image.size
        x = int(random.uniform(0, w))
        y = int(random.uniform(0, h))
        return (x,y)

    # XXX: Todo: is it possible to generate rects outside the image?
    def random_rects(self, pos=(100,100), max_size=500, tries=10):
        rects = []
        for i in range(tries):
            w0 = int(random.uniform(-1*max_size/2, max_size/2))
            h0 = int(random.uniform(-1*max_size/2, max_size/2))

            w1 = int(random.uniform(-1*max_size/2, max_size/2))
            h1 = int(random.uniform(-1*max_size/2, max_size/2))

            p0 = DrawShape.add_tuple(pos, (w0,h0))
            p1 = DrawShape.add_tuple(pos, (w1,h1))

            rects.append((p0,p1))
        return rects

    


    def stage_draw(self, rect, color):
        staged_image = self.image.copy()
        staged_draw = ImageDraw.Draw(staged_image, 'RGBA')
        # print rect
        staged_draw.rectangle(rect, fill=color)
        return staged_image

    def commit_draw(self, staged_image):
        self.image = staged_image.copy() # remove copy later


    # def draw_rect(self, size, color):
    #     p0 = self.random_pos()
    #     p1 = DrawShape.add_tuple(p0, size)
    #     r,g,b = self.og_image.getpixel(p0)
    #     self.draw.rectangle([p0, p1], fill=(r,g,b,self.alpha), outline=None)

    def draw_rect_rand(self, size):
        pass

    def draw_circle(self, size):
        p0 = self.random_pos()
        p1 = DrawShape.add_tuple(p0, size)
        r,g,b = self.og_image.getpixel(p0)
        self.draw.ellipse([p0, p1], fill=(r,g,b,self.alpha), outline=None)


    
