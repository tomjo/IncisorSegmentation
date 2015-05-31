import math
import numpy as np

def pca(X, nb_components=0):
    '''
    Do a PCA analysis on X
    @param X:                np.array containing the samples
                             shape = (nb samples, nb dimensions of each sample)
    @param nb_components:    the nb components we're interested in
    @return: return the nb_components largest eigenvalues and eigenvectors of the covariance matrix and return the average sample 
    '''
    [n,d] = X.shape
    if (nb_components <= 0) or (nb_components>n):
        nb_components = n
    means = X.mean(axis=0)
    X -= means
    cov = X.dot(X.transpose()) / n
    
    eigVals, eigVectors = np.linalg.eigh(cov)
  
    #sort and take nb_component highest eigenvalues/vectors
    sortedEigVals = sorted(eigVals, reverse=True)
    sortedEigVectors = np.zeros_like(eigVectors)
    idx = len(sortedEigVals)-1
    for i in range(len(sortedEigVals)):
        sortedEigVectors[:,i] = eigVectors[:, idx]
        idx -= 1
    sortedEigVals = np.array(sortedEigVals)[:nb_components]
    sortedEigVectors = X.transpose().dot(sortedEigVectors)

    #normalize
    sortedEigVectors = sortedEigVectors.transpose()
    res = []
    for i in range(sortedEigVectors.shape[0]):
        suma = math.sqrt(sum([j**2 for j in sortedEigVectors[1]]))
        res.append([j/suma for j in sortedEigVectors[i]])
    sortedEigVectors = np.array(res).transpose()
    
    return sortedEigVals, sortedEigVectors, means