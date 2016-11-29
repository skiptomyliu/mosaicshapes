from PIL import Image, ImageDraw, ImageChops
import random
import math
from util import *
from copy import copy, deepcopy
from rect import Rect

class DrawShape(object):

    def __init__(self, imgpath):
        self.og_image = Image.open(imgpath)
        self.image = Image.new('RGB', self.og_image.size)
        self.draw = ImageDraw.Draw(self.image, 'RGBA')
        self.alpha = 110

        w,h = self.image.size
        t_r = Rect.init_coords(self.image.size,[(0,0), (w,h)])
        self.draw_shape(t_r, average_color(t_r.coords(), self.og_image))

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

    
    def get_staged_diff(self, shape, color):
        staged_image = self.stage_draw(shape, color)
        return DrawShape.rmsdiff(self.og_image, staged_image)

    def stage_draw(self, rect, color):
        staged_image = self.image.copy()
        staged_draw = ImageDraw.Draw(staged_image, 'RGBA')
        staged_draw.rectangle(rect.coords(), fill=color)
        return staged_image

    def draw_shape(self, shape, color):
        self.draw.rectangle(shape.coords(), fill=color)


    def find_best_alpha(self, rect, tries=10):
        r,g,b = average_color(rect.coords(), self.og_image)
        alpha = 10
        best_color = (r,g,b,alpha)
        best_image = self.stage_draw(rect, best_color)
        staged_image = best_image.copy()
        best_diff = DrawShape.rmsdiff(self.og_image, staged_image)
        for i in range(tries):
            alpha = random.randint(100, 255)
            color = (r,g,b,alpha)

            staged_image = self.stage_draw(rect, color)
            cur_diff = DrawShape.rmsdiff(self.og_image, staged_image)
            if cur_diff < best_diff:
                best_diff = cur_diff
                best_color = color

        return best_color

    def find_best_shape(self, tries=100):
        best_rect = Rect(self.image.size)
        best_image = self.stage_draw(best_rect, average_color(best_rect.coords(), self.og_image))
        staged_image = best_image.copy()
        best_diff = DrawShape.rmsdiff(self.og_image, staged_image)
        for i in range(tries):
            temp_rect = Rect(self.image.size)
            staged_image = self.stage_draw(temp_rect, average_color(temp_rect.coords(), self.og_image))
            cur_diff = DrawShape.rmsdiff(self.og_image, staged_image)
            if cur_diff < best_diff:
                best_diff = cur_diff
                best_rect = copy(temp_rect)
                print best_rect, best_rect.area()

        return best_rect

    def find_best_mutate(self, rect, tries=50):
        color = average_color(rect.coords(), self.og_image)
        best_image = self.stage_draw(rect, color)
        staged_image = best_image.copy()
        best_diff = DrawShape.rmsdiff(self.og_image, staged_image)
        best_rect = copy(rect)
        best_color = color

        for i in range(tries):
            temp_rect = copy(rect)
            temp_rect.mutate()
            color = average_color(temp_rect.coords(), self.og_image)

            staged_image = self.stage_draw(temp_rect, color)
            cur_diff = DrawShape.rmsdiff(self.og_image, staged_image)
            if cur_diff < best_diff:
                best_diff = cur_diff
                best_rect = copy(temp_rect)
                best_color = color
                rect = best_rect

                print "best diff"
                print best_diff
                # print best_rect
                print best_rect.area()

        return (best_rect, best_color)
