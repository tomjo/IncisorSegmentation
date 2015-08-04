import copy
from Case import Incisor
import numpy as np
import Util
import types

class ASM():
    
    def __init__(self, lm):
        self.lm = lm
        self.meanShape = None
    
    def meanModel(self):
        if isinstance(self.lm, types.ListType):
            return np.mean(self.getMatrix(), axis=0)
        return np.mean(self.lm, axis=0)
              
    def getMatrix(self):
        m = []
        for i in self.lm:
            m.append(np.hstack(i.lm))
        return np.array(m)
    
    def matrixToObjects(self):
        incisors = []
        for ind in range(len(self.lm)):
            incisor = Incisor(None)
            incisor.readVector(self.lm[ind, :])
            incisors.append(incisor)
        self.lm = incisors
                    
    def align(self):
        self.matrixToObjects()
        for i in self.lm:
            i.translateToOrigin()
        for i in self.lm:
            i.scaleToUnit()  
        
        self.meanShape = copy.copy(self.lm[0])
        oldMeanShape = Incisor(None)
        oldMeanShape.readMatrix(np.zeros_like(self.meanShape.lm))
        
        while not Util.isConverged(oldMeanShape, self.meanShape):
            oldMeanShape.readMatrix(self.meanShape.lm)
            self.meanShape.readVector(self.meanModel())
            
            self.meanShape.translateToOrigin()
            self.meanShape.scaleToUnit()
            
            for i in self.lm:
                angle = Util.calcRotation(self.meanShape, i)
                i.rotate(angle)
                if i.distanceToOrigin() != .1:
                    i.translateToOrigin()
                    
        meanScaleFactor = 0
        for i in self.lm:
            meanScaleFactor += i.scaleFactor
        self.meanShape.scaleFactor = meanScaleFactor / float(len(self.lm))
        
    def rescaleAndRealign(self):
        for i in self.lm:
            i.scale(self.meanShape.scaleFactor)
            i.realignToAbsolute()
        self.meanShape.scaleBack()
        self.meanShape.realignToAbsolute()
    