import numpy as np
from math import cos, sin, sqrt
from numbers import Number

working_precision = 1e-15

class Point():

    def __init__(self, x=0.0, y=0.0):
        if isinstance(x,Number) and isinstance(y,Number):
            self.x = x
            self.y = y
        else:
            self.x = x[0]
            self.y = x[1]
    
    def __add__(self, other):
        return Point(self.x + other[0], self.y + other[1])

    def __sub__(self, other):
        if isinstance(other,Number):
            return Point(self.x - other, self.y - other)
        else:
            return Point(self.x - other[0], self.y - other[1])

    def __mul__(self, other):
        if isinstance(other,Number):
            return Point(self.x*other, self.y*other)
        else:
            return Point(self.x*other[0], self.y*other[1])
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __rmul__(self, other):
        return self.__mul__(other)

    def __abs__(self):
        return sqrt(self.x**2 + self.y**2)

    def __eq__(self, other):
        return self.x == other[0] and self.y == other[1]

    def __ne__(self, other):
        return not self.__eq__(other)  # reuse __eq__
    
    def __str__(self):
        return "Point(%.2f,%.2f)"%(self.x,self.y)
    
    def __getitem__(self, key):
        if key == 0 or key == "x":
            return self.x
        elif key == 1 or key == "y":
            return self.y
        else:
            raise LookupError("Class point does not contain index %s"%str(key))
    
    def __setitem__(self, key, value):
        if key == 0 or key == "x":
            self.x = value
        elif key == 1 or key == "y":
            self.y = value
        else:
            raise LookupError("Class point does not contain index %s"%str(key))
    
    def __len__(self):
        return 2
    
    def __delitem__(self, key):
        if key == 0 or key == "x":
            self.x = None
        elif key == 1 or key == "y":
            self.y = None
        else:
            raise LookupError("Class point does not contain index %s"%str(key))
    
    def __iter__(self):
        yield self.x
        yield self.y
        raise StopIteration
    
    def move(self, dx=1.0, dy=1.0):
        # Convert to geom classes if lists given
        if type(dx) in [list, tuple, Vector]:
            dx, dy = dx
        self.x += dx
        self.y += dy
    

if __name__ == "__main__":
    point = Point([1,2.0])
    print(point)

    point.move(100,100)
    print(point)
