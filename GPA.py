import numpy as np

def generalizedProcrustesAnalysis(shapes, threshold=0.00001):
    tmp = shapes.astype(float)
    
    mean = tmp[0]
    done = False
    while not done:
        #normalize translation -> all centers to origin
        tmp = map(centerOrigin, tmp)
        #normalize scale
        tmp = map(normalizeScale, tmp)
        #normalize rotation -> rotation of each shape aligned with current mean
        tmp = [alignRotation(shape, mean) for shape in tmp]
        nextMean = sum(shape for shape in tmp) / len(tmp)
        done = all([m - n < threshold for (m,n) in zip(nextMean.flatten(), mean.flatten())])
        mean = nextMean
    
    tmp = [alignRotation(shape, mean) for shape in tmp]
    return mean,tmp

def centerOrigin(s):
    #align shape to origin
    return s - s.mean(0)
    
def normalizeScale(s):
    #scale shape by 1/norm(shape)
    return s.astype(float) / np.linalg.norm(s)
    
def alignRotation(s1, s2):
    #returns the first shape aligned to the second shape
    #rotation = svd
    u,s,v = np.linalg.svd(np.dot(s2.conj().transpose(), s1))
    v = v.conj().transpose()
    u = u.conj().transpose()
    return np.dot(np.dot(s1, v), u)