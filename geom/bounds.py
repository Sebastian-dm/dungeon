import numpy as np
from math import sqrt, hypot

from .point import Point

class Bounds():

    def __init__(self, x_range=[0,1], y_range=[0,1]):
        """ Bounds object for checking whether geometry is inside or outside
        Input:
            x_range: list or tuple containing x_min and x_max
            y_range: list or tuple containing y_min and y_max
        """
        self.x_range = sorted(np.array(x_range))
        self.y_range = sorted(np.array(y_range))
        
        self.width = x_range[1]-x_range[0]
        self.height = y_range[1]-y_range[0]

        self.midpoint = Point()
    
    def __str__(self):
        return "Bounds(x-range=%s, y-range=%s)"%(self.x_range, self.y_range)
    
    def area(self):
        return self.width * self.height
    
    def contains(self, geom):
        if type(geom) == Point:
            if self.x_range[0] <= geom.x <= self.x_range[1] and \
               self.y_range[0] <= geom.y <= self.y_range[1]:
                return True
        elif type(geom) == Line:
            if self.x_range[0] <= geom.start.x <= self.x_range[1] and \
               self.y_range[0] <= geom.start.y <= self.y_range[1] and \
               self.x_range[0] <= geom.end.x <= self.x_range[1] and \
               self.y_range[0] <= geom.end.y <= self.y_range[1]:
                return True
        else:
            raise Exception("Unknown geometry class")
        return False


if __name__ == "__main__":
    bounds = Bounds([0,10],[0,10])
    print("Created:",bounds)
    print("Area:",bounds.area())

    p1 = Point([0.5,11])
    l1 = Line([0,0],[10,11])
    print(bounds.contains(l1))



