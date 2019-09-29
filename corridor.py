from random import choice

from geom.line import Line
from geom.point import Point
from settings import corridor_width

class Corridor(Line):

    def __init__(self, *args):
        super(Corridor, self).__init__(*args)
        self._set_width()

    def __str__(self):
        return "Corridor(start=%s, end=%s)"%(self.start,self.end)
    
    def _set_width(self):
        table_result = choice(corridor_width)
        self.width = table_result
        


if __name__ == "__main__":
    corridor = Corridor([0,0],[10,10])
    print("Created:",corridor)
    print("Length:",corridor.length())

    corridor2 = Corridor([10,0],[-0.5, 0.5], 14)
    print("Created:",corridor)

    intersection = corridor.intersects(corridor2)
    print(intersection)
