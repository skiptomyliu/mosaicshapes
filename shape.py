


import abc

class Shape(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def coords(self):
        return

    @abc.abstractmethod
    def random(self):
        return
    
    @abc.abstractmethod
    def mutate(self):
        return