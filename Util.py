import cv
import Shape
import Point
import fnmatch
import os
import cv2

def loadLandmarks(incisor,dirname='Landmarks/Original/', excl=[]):
    pts = []
    files = fnmatch.filter(os.listdir(dirname), "*-{}.txt".format(str(incisor)))
    cases = [i for i in range(len(files)) if (i+1) not in excl]
    for i in cases:
        pts.append(_loadLandmarks(dirname+files[i]))
    return pts 
    
def _loadLandmarks(file):
    s = Shape.Shape([])
    lines  = open(file).readlines()
    for i in range(0, len(lines), 2):
        s.addPoint(Point.Point(float(lines[i+1].strip()), float(lines[i].strip())))
    return s  
    
def loadImage(caseId, dirname='Radiographs/'):
    return cv2.imread(dirname+caseId+'.tif')
    #return cv.LoadImage(dirname+caseId+'.tif')
    
def drange(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step
    