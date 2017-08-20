
import util
import numpy as np
from enum import Enum
import abc
import random
from random import shuffle, randint

class Quadrant(Enum):
    top_left = 1
    top_right = 2
    bottom_right = 3
    bottom_left = 4


class Direction(Enum):
    top = 1
    right = 2
    bottom = 3
    left = 4

class Cell(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        print "I am init"



    @abc.abstractmethod
    def find_best(self):
        return
    
    @abc.abstractmethod
    def draw(self):
        return

    