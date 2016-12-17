
import util
import numpy as np

import abc
class Cell(object):
    __metaclass__ = abc.ABCMeta

    @staticmethod
    def gen_colors(base_color, n):
        deg = 30/360.0
        colors = []
        if n==1:
            if isinstance(base_color, (np.ndarray, np.generic)):
                base_color = tuple(base_color.astype(int))
            colors.append(base_color)
        else:   
            # maximum distance between all colors combined
            distance = 40
            colors = []

            r,g,b = base_color
            quad = 1 if util.luminance(r,g,b) > 100 else 0
            for i in range(-n/2+quad, n/2+quad):
                color = np.asarray(base_color) + (i)*distance/float(n)
                color[0] = util.clamp_int(color[0], 0, 255)
                color[1] = util.clamp_int(color[1], 0, 255)
                color[2] = util.clamp_int(color[2], 0, 255)
                color = tuple(color.astype(int))
                colors.append(color)

        return colors


    @abc.abstractmethod
    def find_best(self):
        return
    
    @abc.abstractmethod
    def draw(self):
        return

    