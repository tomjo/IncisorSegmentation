import math
import numpy as np
import fnmatch
from Case import Incisor
import os

def calcRotation(shape, curShape):
    a = 0.
    b = 0.
    for i in range(len(shape.lm)):
        a += curShape.lm[i,0] * shape.lm[i,1] - curShape.lm[i,1] * shape.lm[i,0]
        b += curShape.lm[i,0] * shape.lm[i,0] - curShape.lm[i,1] * shape.lm[i,1]
    return math.atan2(a,b)
    
def isConverged(prevShape, newShape, threshold=0.0000001):
    diff = newShape.lm - prevShape.lm
    diff = diff**2
    maxChange = np.max(diff)
    return maxChange < threshold
    
def getIncisorVectors(incisorNum):
    files = fnmatch.filter(os.listdir('Landmarks/original/.'), "*-{}.txt".format(str(incisorNum)))
    vectors = np.zeros((len(files), 80))
    for i in range(len(files)):
        incisor = Incisor.fromFile('Landmarks/original/'+files[i])
        vectors[i,:] = np.hstack(incisor.lm)
    return vectors;