import numpy as np
from math import cos, sin, sqrt
from numbers import Number


a=np.array([1,2]) 

working_precision = 1e-15

class Vector():

    def __init__(self, x=0.0, y=0.0):
        if isinstance(x,Number) and isinstance(y,Number):
            self.x = x
            self.y = y
        else:
            self.x = x[0]
            self.y = x[1]
    
    def __add__(self, other):
        return Vector(self.x + other[0], self.y + other[1])

    def __sub__(self, other):
        return Vector(self.x - other[0], self.y - other[1])

    def __mul__(self, other):
        if isinstance(other,Number):
            return Vector(self.x*other, self.y*other)
        else:
            return self.x*other[0] + self.y*other[1]
    
    def __rmul__(self, other):
        return self.__mul__(other)

    def __abs__(self):
        return sqrt(self.x**2 + self.y**2)

    def __eq__(self, other):
        return self.x == other[0] and self.y == other[1]

    def __ne__(self, other):
        return not self.__eq__(other)  # reuse __eq__
    
    def __str__(self):
        return "Vector(%s,%s)"%(self.x,self.y)
    
    def __getitem__(self, key):
        if key == 0 or key == "x":
            return self.x
        elif key == 1 or key == "y":
            return self.y
        else:
            raise LookupError("Class vector does not contain index %s"%str(key))
    
    def __setitem__(self, key, value):
        if key == 0 or key == "x":
            self.x = value
        elif key == 1 or key == "y":
            self.y = value
        else:
            raise LookupError("Class vector does not contain index %s"%str(key))
    
    def __len__(self):
        return 2
    
    def __delitem__(self, key):
        if key == 0 or key == "x":
            self.x = None
        elif key == 1 or key == "y":
            self.y = None
        else:
            raise LookupError("Class vector does not contain index %s"%str(key))
    
    def __iter__(self):
        yield self.x
        yield self.y
        raise StopIteration
    
    def rotate(self, angle, unit="rad"):
        # Convert to radians
        if unit == "deg":
            if angle == 90:
                angle = np.pi/2
            elif angle == 180:
                angle = np.pi
            else:
                angle = np.radians(angle)
        # Build Rotation
        c, s = np.cos(angle), np.sin(angle)
        R = np.array(((c,-s), (s, c)))
        # Rotate
        coords = np.array([self.x,self.y])
        coords = R.dot(coords)
        coords[np.abs(coords) < working_precision] = 0
        self.x, self.y = coords
        return self
    
    def rotated(self, angle, unit="rad"):
        new_vector = Vector(self).rotate(angle, unit)
        return new_vector

    
    def length(self):
        return sqrt(self.x**2+self.y**2)

    def normalize(self):
        self.coords = self.coords / self.length()
        return self
    
    def set_length(self, length):
        self_length = self.length()
        self.x *= length/self_length
        self.y *= length/self_length
        return self

if __name__ == "__main__":
    vector = Vector([15,2.0])

    # Get item
    print("Get item 1 and 2:",vector[0], vector[1])

    # Set item
    vector[0] = 1.0
    vector[1] = 0.0

    # Iterate
    for c in vector:
        print(c)
    
    print("Length:",vector.length())
    
    # Rotate
    print(vector)
    print("Rotating 90 deg")
    vector.rotate(90,"deg")
    print(vector)
    print(5*vector)