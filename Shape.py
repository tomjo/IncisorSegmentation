import numpy as np
import Point
import math

class Shape( object ):
   
    def __init__(self, lm = []): 
        self.points = lm
    
    def addPoint(self, point):
        self.points.append(point)
 
    def getVector(self):
        vec = np.zeros((len(self.points), 2))
        for i in range(len(self.points)):
            vec[i,:] = [self.points[i].x, self.points[i].y]
        return vec.flatten()

    def getNormalToPoint(self, pIdx):
        x = 0; y = 0; mag = 0
        if pIdx == 0: #first point
            x = self.points[1].x - self.points[0].x
            y = self.points[1].y - self.points[0].y
        elif pIdx == len(self.points)-1: #last point
            x = self.points[-1].x - self.points[-2].x
            y = self.points[-1].y - self.points[-2].y
        else:
            x = self.points[pIdx+1].x - self.points[pIdx-1].x
            y = self.points[pIdx+1].y - self.points[pIdx-1].y
        mag = math.sqrt(x**2 + y**2)
        return (-y/mag, x/mag)
    
    @staticmethod
    def fromVector(vec):
        s = Shape([])
        for i,j in np.reshape(vec, (-1,2)):
            s.addPoint(Point.Point(i, j))
        return s
        
    def __add__(self, other):
        s = Shape([])
        for i,p in enumerate(self.points):
            s.addPoint(p + other.points[i])
        return s

    def __div__(self, i):
        s = Shape([])
        for p in self.points:
            s.addPoint(p/i)
        return s
    
    def __eq__(self, other):
        for i in range(len(self.points)):
            if self.points[i] != other.points[i]:
                return False
        return True
    
    def __ne__(self, other):
        return not self.__eq__(other)