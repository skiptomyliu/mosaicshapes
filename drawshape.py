from PIL import Image, ImageDraw, ImageChops
import random
import math
from util import *
from copy import copy, deepcopy

class DrawShape(object):

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
    def rmsdiff(im1, im2):
        diff = ImageChops.difference(im1, im2)
        h = diff.histogram()
        sq = (value*((idx%256)**2) for idx, value in enumerate(h))
        sum_of_squares = sum(sq)
        rms = math.sqrt(sum_of_squares/float(im1.size[0] * im1.size[1]))
        return rms

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
        staged_draw.rectangle(rect.coords(), fill=color)
        return staged_image

    def commit_draw(self, staged_image):
        self.image = staged_image.copy() # remove copy later


    def find_best(self, rect, tries=50):
        color = average_color(rect, self.og_image)
        best_image = self.stage_draw(rect, color)
        staged_image = best_image.copy()
        best_diff = DrawShape.rmsdiff(self.og_image, staged_image)
        best_rect = copy(rect)
        best_color = color
        # print "should be same"
        # print best_diff
        # import pdb; pdb.set_trace()

        for i in range(tries):
            temp_rect = copy(rect)
            temp_rect.mutate()
            color = average_color(temp_rect, self.og_image)
            staged_image = self.stage_draw(temp_rect, color)
            cur_diff = DrawShape.rmsdiff(self.og_image, staged_image)
            if cur_diff < best_diff:
                best_diff = cur_diff
                best_rect = copy(temp_rect)
                best_color = color
                
                # print "best diff"
                # print best_diff
                # print best_rect
                # print best_rect.area()

        return (best_rect, best_color)
