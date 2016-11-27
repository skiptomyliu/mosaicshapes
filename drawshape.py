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

    def random_pos(self):
        w,h = self.image.size
        x = random.uniform(0, w)
        y = random.uniform(0, h)
        return (x,y)


    def draw_rect(self, size):
        p0 = self.random_pos()
        p1 = DrawShape.add_tuple(p0, size)
        r,g,b = self.og_image.getpixel(p0)
        self.draw.rectangle([p0, p1], fill=(r,g,b,self.alpha), outline=None)

    def draw_circle(self, size):
        p0 = self.random_pos()
        p1 = DrawShape.add_tuple(p0, size)
        r,g,b = self.og_image.getpixel(p0)
        self.draw.ellipse([p0, p1], fill=(r,g,b,self.alpha), outline=None)

    def draw_rect_rand_size(self):
        w = random.uniform(self.min_size, self.max_size)
        h = random.uniform(self.min_size, self.max_size)
        size = (w,h)
        # print w,h
        self.draw_rect(size)

        sub_0 = random.uniform(1, self.sub_max_by)
        sub_1 = random.uniform(1, self.sub_max_by)
        if self.max_size - sub_0 > 0:
            self.max_size -= sub_0
        if self.min_size - sub_1 > 0:
            self.min_size -= sub_1

        print self.max_size, self.min_size
        # import pdb; pdb.set_trace()
        # print self.max_size
        # print self.min_size
        # self.image.show()

    @staticmethod
    def add_tuple(p0, p1):
        return tuple(sum(x) for x in zip(p0, p1))

    @staticmethod
    def rmsdiff(im1, im2):
        diff = ImageChops.difference(im1, im2)
        h = diff.histogram()
        sq = (value*((idx%256)**2) for idx, value in enumerate(h))
        sum_of_squares = sum(sq)
        rms = math.sqrt(sum_of_squares/float(im1.size[0] * im1.size[1]))
        return rms
