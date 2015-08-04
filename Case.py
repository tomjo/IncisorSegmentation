import numpy as np
import copy
import os

class Incisor:
    
    def __init__(self,lm):
        self.lm = lm
        if self.lm is None:
            self.lm = []
        self.normalized = np.empty((40,2), np.int32)
        self.centroid = None
        self.oldCentroid = None
        self.scales = []
        self.scaleFactor = None
        if lm is not None:
            self.calcCentroid(None)
    
    '''
    @classmethod
    def fromId(cls, caseId, id):
        f  = open('Landmarks/original/landmarks'+str(caseId)+'-'+str(id)+'.txt', 'r')
        tmp = []
        lm = np.empty((40,2), np.int32) 
        for line in f:
            tmp = tmp+[int(float(line))]
        for x in range(40):
            lm[x] = tmp[2*x],tmp[2*x+1] 
        c = cls(lm) 
        c.id = id
        c.caseId = caseId
        return c
        '''
    
    @classmethod
    def fromFile(cls, f):
        lines  = open(f).readlines()
        tmp = []
        for i in range(0, len(lines), 2):
            tmp.append(np.array([float(lines[i+1].strip()), float(lines[i].strip())]))
        tmp = np.array(tmp)
        c = cls(tmp)
        return c
        
    #m = points in matrix format: [[y_1, x_1], [y_2, x_2], ..., [y_n, x_n]]
    def readMatrix(self, m, weights=None):
        self.lm = copy.copy(m)
        self.calcCentroid(weights)
        
    #v = vector of points in opencv mapping style:  [y_1, x_1, ..., y_n, x_n], numpy array
    def readVector(self, v, weights=None):
        self.lm = np.zeros((len(v) / 2, 2))
        self.lm[:, 0] = copy.copy(v[range(0, len(v), 2)])
        self.lm[:, 1] = copy.copy(v[range(1, len(v), 2)])
        self.calcCentroid(weights)
                                                                                                                                    
    def calcCentroid(self, weights=None):
        if weights is None:
            self.centroid = np.mean(self.lm, 0)
        else:
            self.centroid = np.zeros((1, len(self.lm[0])))
            for i in range(len(self.lm)):
                self.centroid += self.lm[i, :] * weights[i]
            #self.centroid = self.centroid.dot(1. / weights.sum())
            
    def translateToOrigin(self, weights=None):
        if weights is None:
            centroid = np.mean(self.lm, 0)
        else:
            centroid = np.zeros((1, len(self.lm[0])))
            for i in range(len(self.lm)):
                centroid += self.lm[i, :] * weights[i]
            centroid = centroid.dot(1. / weights.sum())
            
        self.lm -= centroid
        self.oldCentroid = centroid
        self.calcCentroid(weights)
                        
    def translateTo(self, centroid, weights):
        self.lm += centroid
        self.calcCentroid(weights)
        
    def scaleToUnit(self):
        #scaletounit = divide by l2 norm (could replace this with np.linalg.norm?)
        self.scaleFactor = np.power(self.lm - self.centroid, 2);
        self.scaleFactor = np.sqrt(self.scaleFactor.dot(1. / len(self.lm)).sum())
        self.lm = self.lm.dot(1. / self.scaleFactor)
        self.calcCentroid()
        
    def scaleBack(self):
        self.lm = self.lm.dot(self.scaleFactor)
 
    def scale(self, factor):
        self.lm = self.lm.dot(factor)
        
    def rotate(self, angle):
        m = np.array([[np.cos(angle), np.sin(angle)], [-np.sin(angle), np.cos(angle)]])
        for i in range(len(self.lm)):
         self.lm[i, :] = self.lm[i, :].dot(m)
    
    def alignRotationWith(self, shape):
        u,s,v = np.linalg.svd(np.dot(shape.conj().transpose(), self.lm))
        v = v.conj().transpose()
        u = u.conj().transpose()
        self.lm = np.dot(np.dot(self.lm, v), u)
        
    def realignToAbsolute(self):
        minimums = np.min(self.lm, axis=0)
        self.lm = self.lm - minimums
        
    def distanceToOrigin(self):
        dst = np.power(self.lm - self.centroid, 2)
        dst = dst.dot(1./len(self.lm)).sum()
        return np.sqrt(dst)                                            
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
    def printTxt(self):
        print "Incisor "+str(self.id)+" from case "+str(self.caseId)+", landmarks: ", self.lm

class Case:
    
    def __init__(self, caseId):
        print "dowe"
        self.caseId = caseId;
        self.incisors = [Incisor.fromId(caseId, id) for id in range(1,9)]
    
    def printTxt(self):
        print "Case "+str(self.caseId)
        
                 

                