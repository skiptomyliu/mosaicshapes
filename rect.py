


from shape import Shape
import random
from util import *

class Rect(Shape):
    def __init__(self, bound_size):
        self.bound_size = bound_size
        self.x0 = -1
        self.y0 = -1
        self.x1 = -1
        self.y1 = -1

        self.random()

    def coords(self):
        return [(self.x0, self.y0), (self.x1, self.y1)]

    def area(self):
        w = abs(self.x0 - self.x1)
        h = abs(self.y0 - self.y1)

        # print self.x0,self.x1,self.y0,self.y1
        if w*h == 0:
            import pdb ;pdb.set_trace()
        return w*h

    def random(self):
        while True:
            w,h = self.bound_size
            self.x0 = int(random.randint(0, w-1))
            self.y0 = int(random.randint(0, h-1))
            self.x1 = clamp_int(self.x0 + random.randint(0, 64) + 1, 0, w-1)
            self.y1 = clamp_int(self.y0 + random.randint(0, 64) + 1, 0, h-1)

            if int(self.x0) != int(self.x1) and int(self.y0) != int(self.y1):
                break;
            else:
                self.random()

        # print self.area()
        # print self.x0,self.x1,self.y0,self.y1

    def mutate(self):
        w,h = self.bound_size

        while True:
            if bool(random.getrandbits(1)):
                self.x0 = clamp_int(self.x0+random.randint(0, 32), 0, w-1)
                self.y0 = clamp_int(self.y0+random.randint(0, 32), 0, h-1)
            else:
                self.x1 = clamp_int(self.x1+random.randint(0, 32), 0, w-1)
                self.y1 = clamp_int(self.y1+random.randint(0, 32), 0, h-1)


            # if bool(random.getrandbits(1)):
            #     if bool(random.getrandbits(1)):
            #         self.x0 = clamp_int(self.x0+random.uniform(0, 16), 0, w-1)
            #     else:
            #         self.x0 = clamp_int(self.x0-random.uniform(0, 16), 0, w-1)

            #     if bool(random.getrandbits(1)):
            #         self.y0 = clamp_int(self.y0+random.uniform(0, 16), 0, h-1)
            #     else:
            #         self.y0 = clamp_int(self.y0-random.uniform(0, 16), 0, h-1)
            # else:
            #     if bool(random.getrandbits(1)):
            #         self.x1 = clamp_int(self.x1+random.uniform(0, 16), 0, w-1)
            #     else:
            #         self.x1 = clamp_int(self.x1-random.uniform(0, 16), 0, w-1)

            #     if bool(random.getrandbits(1)):
            #         self.y1 = clamp_int(self.y1+random.uniform(0, 16), 0, h-1)
            #     else:
            #         self.y1 = clamp_int(self.y1-random.uniform(0, 16), 0, h-1)

            # # print self
            if int(self.x0) != int(self.x1) and int(self.y0) != int(self.y1):
                print self
                break;
            else:
                self.random()


    def __str__(self):
        return "({x},{y}),({x1},{y1})".format(x=self.x0, y=self.y0, x1=self.x1, y1=self.y1)

