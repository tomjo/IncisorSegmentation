import numpy as np
from sklearn.decomposition import PCA
import math

class VarianceModel():
    #creates the variancemodel, asm needs to be aligned, rescaled and realigned
    def __init__(self, asm):
        self.asm = asm
        self.deviation = asm.getMatrix()
        self.covariance = None
        self.pca = None

        for ind in range(len(self.deviation)):
            self.deviation[ind, :] = self.deviation[ind, :] - asm.meanModel()
 
    def doPCA(self):
        if self.covariance is None:
            self.covariance = np.cov(self.deviation, rowvar=0)
        if self.pca is None:
            self.pca = PCA(n_components=3)
            self.pca.fit(self.deviation)
        return (self.eigenValues(),self.pca.components_)
        
    def varianceRatio(self):
        if self.pca is None:
            self.pca = PCA(n_components=3)
            self.pca.fit(self.deviation)
        return self.pca.explained_variance_ratio_

    def eigenValues(self):
        if self.covariance is None:
            self.covariance = np.cov(self.deviation, rowvar=0)
        if self.pca is None:
            self.pca = PCA(n_components=3)
            self.pca.fit(self.deviation)
        eigenvals = np.linalg.eigvalsh(self.covariance)
        return sorted(eigenvals, reverse=True)[:len(self.pca.components_)]

    def fit(self, componentIdx, interpolationCount):
        eigenvalues, components = self.doPCA()
        components = components.transpose()
        shapes = np.zeros((interpolationCount, len(components)))
        step = 2. * 3. * math.sqrt(eigenvalues[componentIdx])/interpolationCount
        for step_ind in range(interpolationCount):
            b = np.zeros((len(components[0]), 1))
            b[componentIdx] = -3. * math.sqrt(eigenvalues[componentIdx]) + step * step_ind  
            shapes[step_ind, :] = np.hstack(self.asm.meanShape.lm) + components.dot(b).transpose()
        return shapes