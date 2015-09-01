import numpy as np
import Shape
import Point

#aligns first to second shape
def alignToShape(s1,s2,w):
    params = getPoseParams(s1, s2, w)
    return applyPoseParams(s1, params)
    
"""
Applies scaling/translation/rotation to each point in shape to align it to the other shape

Solve
[ X2 -Y2  W   0 ][ax]   [X1]
[ Y2  X2  0   W ][ay] = [Y1]
[ Z   0   X2  Y2][tx]   [C1]
[ 0   Z  -Y2  X2][ty]   [C2]
to find ax, ay, tx, ty

"""
def getPoseParams(s1, s2, w):
    X1 = _calcX(s2, w)
    X2 = _calcX(s1, w)
    Y1 = _calcY(s2, w)
    Y2 = _calcY(s1, w)
    Z = _calcZ(s1, w)
    W = sum(w)
    C1 = _calcC1(s1, s2, w)
    C2 = _calcC2(s1, s2, w)

    a = np.array([[ X2, -Y2,   W,  0],
                  [ Y2,  X2,   0,  W],
                  [  Z,   0,  X2, Y2],
                  [  0,   Z, -Y2, X2]])

    b = np.array([X1, Y1, C1, C2])
    # returns [ax, ay, tx, ty]
    return np.linalg.solve(a, b)

def applyPoseParams(shape, params):    
    s = Shape.Shape([])
    for p in shape.points:
        x = (params[0]*p.x - params[1]*p.y) + params[2]
        y = (params[1]*p.x + params[0]*p.y) + params[3]
        s.addPoint(Point.Point(x,y))       
    return s
         
def _calcX(s1, w):
    return sum([w[i]*s1.points[i].x for i in range(len(s1.points))])
    
def _calcY(s1, w):
    return sum([w[i]*s1.points[i].y for i in range(len(s1.points))])
    
def _calcZ(s1, w):
    return sum([w[i]*(s1.points[i].x**2+s1.points[i].y**2) for i in range(len(s1.points))])

def _calcC1(s1, s2, w):
    return sum([w[i]*(s2.points[i].x*s1.points[i].x + s2.points[i].y*s1.points[i].y) for i in range(len(s1.points))])

def _calcC2(s1, s2, w):
    return sum([w[i]*(s2.points[i].y*s1.points[i].x - s2.points[i].x*s1.points[i].y) for i in range(len(s1.points))])