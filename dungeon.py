import pandas as pd
import numpy as np
from random import choice

from geom.point import Point
from geom.vector import Vector
from geom.bounds import Bounds
from geom.point import Point

from corridor import Corridor
from settings import *


class Dungeon:
    def __init__(self, width=83, height=59):
        """
        input:
            width: width of dungeon canvas in squares
            height: height of dungeon canvas in squares
        """
        # Geometry
        self.canvas = Bounds([0, width], [0, height])
        print("Canvas:", self.canvas)
        self.origin = Point(width/2, height/2)
        print("Origin:", self.origin)

        # Structure data
        self.queue = list()
        self.corridors = []
        self.traps = []
        self.tricks = []
        self.monsters = []

        # Build
        self.build_first_room()

    
    def build_first_room(self):
        for corridor in self.corridors:
            print(corridor)
        """ Initialize dungeon by putting the first structure in queue """
        directions = [Vector(d) for d in [[0,1],[0,-1],[1,0],[-1,0]]]
        locations = [self.origin+l for l in [[0,1],[0,-1],[1,0],[-1,0]]]
        for i in range(len(directions)):
            length = 6
            #print("creating corridor: start=%s, direction=%s, length%s"%(locations[i], directions[i], length))
            self.make_corridor(locations[i], directions[i], length)
            self.plan_construction(self.periodic,
                                   location=locations[i]+length*directions[i],
                                   direction=directions[i])


    def build_dungeon(self, max_iterations=500):
        """ Construct new structures as long as the queue is not empty
            and max number of construction attempts is not reached. """
        attempts = 0
        while self.queue:
            #for const in self.queue:
            #    print(const[0].__name__,const[1],const[2])

            self.construct_next()

            if (attempts+1)%100 == 0:
                print("Attempts:",attempts+1)

            attempts += 1
            if attempts >= max_iterations:
                break
    

    def plan_construction(self, construction, location=None, direction=None):
        """ Add a new structure to the construction queue. If no location
            or direction is given, the current ones will be used. """
        if not location:
            location = self.location
        if not direction:
            direction = self.direction 
        self.queue.append([construction, location, direction])


    def construct_next(self):
        """ Construct the next planned structure from the queue using the
            given location and direction """
        construction = self.queue.pop(0)
        construct_function, location, direction = construction
        construct_function(location, direction)


    def periodic(self, location, direction):
        """ Periodic check is used most often and always in corridors """
        result = choice(table_1A)
        #print(result)

        if result == "proceed":
            self.make_corridor(location, direction, 6)
        elif result == "door":
            0
        elif result == "side_passage":
            self.make_side_passage(location, direction)
        elif result == "turn":
            self.make_turn(location, direction)
        elif result == "chamber":
            0
        elif result == "stair":
            0
        elif result == "end":
            0
        elif result == "trick":
            self.make_trick(location, direction)
        elif result == "trap":
            self.make_trap(location, direction)
        elif result == "monster":
            self.make_monster(location, direction)
        else:
            raise Exception("Unknown periodic check")

    def make_corridor(self, start, direction, distance):
        """ Step a number of squares forward in the current direction"""
        corridor = Corridor(start, direction, distance)
        
        # Check if corridor ends outside the boundary
        if not self.canvas.contains(corridor.end):
            return

        # Check if corridor intersect any other corridor
        for other_corridor in self.corridors:
            intersection = corridor.intersects(other_corridor)
            if intersection != (None,None):
                #print("%s collides with %s"%(corridor, other_corridor))
                return # If close, a check should be made for secret doors
            
        # Save and update
        self.corridors.append(corridor)
        self.plan_construction(self.periodic, corridor.end, direction)
    
    def make_turn(self, location, direction):
        angle = choice(table_1C)
        direction.rotate(angle, "deg")
        self.make_corridor(location, direction, 3)

    def make_side_passage(self, location, direction):
        """ Returns a list of locations and directions of all side passages """
        angles = choice(table_1B)
        for i in range(len(angles)):
            new_direction = direction.rotated(angles[i],"deg")
            self.make_corridor(location, new_direction, 3)

    def make_trap(self, location, direction):
        self.traps.append(location)
        self.make_corridor(location, direction, 3)

    def make_trick(self, location, direction):
        self.tricks.append(location)
        self.make_corridor(location, direction, 3)

    def make_monster(self, location, direction):
        self.monsters.append(location)
        self.plan_construction(self.periodic, location, direction)

    """
    def encloses(self, location):
        # Checks whether a given point is enclosed by the dungeon boundary
        if (     0 <= location[0]
             and 0 <= location[1]
             and location[0] <= self.width/2
             and location[1] <= self.height/2):
            return True
        else:
            return False
    
    
    def corridor_corridor_collisions(self, start, end):
        # Checks whether a corridor collides with any existing corridor
        intersection_points = []
        for i in range(len(self.corridors)):
            ext_corridor = self.corridors.loc[i]
            ext_start = [ext_corridor["X1"], ext_corridor["Y1"]]
            ext_end = [ext_corridor["X2"], ext_corridor["Y2"]]
            intersection_point = line_intersection([start,end],[ext_start,ext_end])

            # Add point to list if an intersection exists
            if intersection_point[0]:
                intersection_points.append(intersection_point)
            
        return intersection_points
    """


if __name__ == "__main__":
    # Setup Parameters
    paper_dimensions = {"A4p":( 595,  842),
                        "A4l":( 842,  595),
                        "A3p":( 842, 1191),
                        "A3l":(1191,  842)}
    width, height = paper_dimensions["A3l"]
    square = 14.2

    width=int(width/square)
    height=int(height/square)
    print("Width:",width,"Height:",height)

    # Make Dungeons
    dungeon = Dungeon(width, height)
    dungeon.build_dungeon()