from Case import Case
from Case import Incisor
import numpy as np
from GPA import *
from PCA import *

if __name__ == '__main__':
    cases = []
    #init cases
    for i in range(1,15):
        cases.append(Case(i))
    #GPA (generalized procrustes analysis) to normalize shapes
    for incisor in range(0,8):
        lmArr = np.empty((2,40,2), dtype=int)
        for case in range(0, len(cases)):
            lmArr = np.concatenate((lmArr,  [cases[case].incisors[incisor].lm]))
            
        (mean,shapes) = generalizedProcrustesAnalysis(lmArr)
        
        for case in range(0, len(cases)):
            cases[case].incisors[incisor].normalized = shapes[case]
            
    #format data for PCA
    ii = 0
    X = np.append(cases[0].incisors[ii].normalized[:,0], cases[0].incisors[ii].normalized[:,1])
    for case in range(1,len(cases)):
        X = np.vstack((X, np.append(cases[case].incisors[ii].normalized[:,0],cases[case].incisors[ii].normalized[:,1])))
    #PCA
    eigenvalues, eigenvectors, mu = pca(X,3)
    
    print 'succ'
            