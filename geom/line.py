import numpy as np
from math import sqrt, hypot

from .point import Point
from .vector import Vector


class Line():

    def __init__(self, *args):
        """ Constructs a line object. If 2 arguments given it is constructed
        between two points. If 3 arguments are given it is constructed from 
        start point, direction vector and length along the vector.
        """
        if len(args) == 2:
            self.by2Points(args[0], args[1])
        elif len(args) == 3:
            self.bySDL(args[0], args[1], args[2])
    
    def by2Points(self, start=Point([0,0]), end=Point([1,1])):
        # Convert to geom classes if lists given
        if type(start) in [list,tuple]:
            start = Point(start)
        if type(end) in [list,tuple]: 
            end = Point(end)
        self.start = start
        self.end = end
        
    def bySDL(self, start=Point(0,0), direction=Vector(1,0), length=2):
        # Convert to geom classes if lists given
        if type(start) in [list, tuple, Vector]:
            start = Point(start)
        if type(direction) in [list, tuple, Point]: 
            direction = Vector(direction)
        
        self.start = start
        
        #Normalize direction vector and set it to correct length
        move_vector = Vector(direction).set_length(length)
        self.end = self.start + move_vector

    
    def __str__(self):
        return "Line(start=%s, end=%s)"%(self.start,self.end)
    
    def length(self):
        line_vector = self.end-self.start
        return hypot(line_vector[0], line_vector[1])
    
    def intersects(self, line):
        """ function computes the point of collision between self and line.
        Input: line

        Returns:
        Tuple of coordinates (x,y,z) for the point of collision. If no collision
        exists, (None,None,None) is returned. """

        # Definitions
        def overlap(a, b):
            return max(0, min(a[1], b[1]) - max(a[0], b[0]))
        
        p, p2 = np.array(self.start), np.array(self.end)
        q, q2 = np.array(line.start), np.array(line.end)
        r = np.subtract(p2, p)
        s = np.subtract(q2, q)
        qpr = np.cross(np.subtract(q, p), r)
        rs = np.cross(r, s)

        # Determine if Directions intersect
        if np.all(rs == 0) and np.all(qpr == 0):
            #lines are colinear (ligger på linie)
            t0 = np.dot(np.subtract(line.start, p), r) / np.dot(r, r)
            t1 = t0 + np.dot(s, r) / np.dot(r, r)
            if overlap([0.,1.], [t0,t1]) > 0:
                # colinear and overlapping (på linie og oveni hinanden)
                return (np.inf, np.inf)
            else:
                # colinear and disjoint (på linie men efter hinanden)
                return (None,None)

        # Determine if Directions intersect
        elif np.all(rs == 0):
            # Parallel and non-intersecting
            return (None,None)

        # Determine if segments intersect
        t = np.divide(np.cross(np.subtract(q,p),s),rs)
        u = np.divide(qpr, rs)
        if not np.all(qpr == 0) and 0 >= t or t >= 1 or 0 >= u or u >= 1:
            # Not parallel but do not intersect
            return (None,None)

        # Calculate point of intersection
        intersection = (line.start + u*s)

        return intersection


if __name__ == "__main__":
    line = Line([0,0],[10,10])
    print(line)

    line2 = Line([10,0],[-0.5, 0.5], 14.14)
    print(line2)

    intersection = line.intersects(line2)
    print(intersection)

