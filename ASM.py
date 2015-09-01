import GPA
import numpy as np
import sys
import Point

class ASM:
    
    def __init__(self, shapes = []):
        self.shapes = shapes
        #self.boundingBox = self.calcBoundingBox()
        self.w = self.calcWeightMatrix()
        self.shapes = GPA.gpa(self.shapes, self.w)
        self.build()
    
    '''
    def calcBoundingBox(self, margin=50):
        if not self.shapes:
            return None
        minX = sys.maxint
        minY = sys.maxint
        maxX = -sys.maxint
        maxY = -sys.maxint
        n = len(self.shapes[0].points)
        for s, shape in enumerate(self.shapes):
            for i in range(n):
                if shape.points[i].x < minX:
                    minX = shape.points[i].x
                if shape.points[i].x > maxX:
                    maxX = shape.points[i].x
                if shape.points[i].y < minY:
                    minY = shape.points[i].y
                if shape.points[i].y > maxY:
                    maxY = shape.points[i].y
        minX -= margin
        minY -= margin
        maxX += margin
        maxY += margin
        return (Point.Point(minX, minY), Point.Point(maxX, maxY))
    '''
            
    def calcWeightMatrix(self):
        if not self.shapes:
            return np.array()
        n = len(self.shapes[0].points)
        
        #distances of each point to each other point in shape
        distances = np.zeros((len(self.shapes), n, n))
        for s, shape in enumerate(self.shapes):
            for i in range(n):
                for j in range(n):
                    distances[s, i, j] = shape.points[i].distance(shape.points[j])
        w = np.zeros(n)
        for i in range(n):
            for j in range(n):
                w[i] += np.var(distances[:, i, j])
        return 1/w     
            
    def build(self, percentCoverage=.98):
        shapeVectors = np.array([s.getVector() for s in self.shapes])
        mean = np.mean(shapeVectors, axis=0)
        #move mean to origin
        mean = np.reshape(mean, (-1,2))
        min_x = min(mean[:,0])
        min_y = min(mean[:,1])
        mean[:,0] = [x - min_x for x in mean[:,0]]
        mean[:,1] = [y - min_y for y in mean[:,1]]
        self.mean = mean.flatten()
    
        #pca
        cov = np.cov(shapeVectors, rowvar=0)
        eigenvalues, eigenvectors = np.linalg.eig(cov)
        variance = np.cumsum(eigenvalues, axis=0) / np.sum(eigenvalues, axis = 0)
        satisfied = (variance > percentCoverage).nonzero()
        self.modes = satisfied[0][1]
        self.eigenvectors = eigenvectors[:self.modes]
        eigenvalues = eigenvalues[:self.modes]
        self.eigenvalues = [e.real for e in eigenvalues]
        for ev in range(self.modes):
            self.eigenvectors[ev] = [e.real for e in self.eigenvectors[ev]]