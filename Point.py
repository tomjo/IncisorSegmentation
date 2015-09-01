import math

class Point( object ):
    
    def __init__(self, x, y):
        if isinstance(x, complex):
            self.x = x.real
        else:
            self.x = x
        if isinstance(y, complex):
            self.y = y.real
        else:
            self.y = y
        
    def distance(self, p):
        return math.sqrt((p.x - self.x)**2 + (p.y - self.y)**2)
        
    def __add__(self, p):
        return Point(self.x + p.x, self.y + p.y)

    def __div__(self, i):
        return Point(self.x/i, self.y/i)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __repr__(self):
        return '(%f, %f)' % (self.x, self.y)