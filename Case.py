import numpy as np

class Incisor:
    
    def __init__(self,caseId,id):
        self.caseId = caseId
        self.id = id
        f  = open('Landmarks/original/landmarks'+str(caseId)+'-'+str(id)+'.txt', 'r')
        tmp = []
        for line in f:
            tmp = tmp+[int(float(line))]
        self.lm = np.empty((40,2), np.int32) 
        self.normalized = np.empty((40,2), np.int32)
        for x in range(40):
            self.lm[x] = tmp[2*x],tmp[2*x+1]
        self.centroid = np.int32(self.lm.mean(0))

    def printTxt(self):
        print "Incisor "+str(self.id)+" from case "+str(self.caseId)+", landmarks: ", self.lm

class Case:
    
    def __init__(self, caseId):
        self.caseId = caseId;
        self.incisors = [Incisor(caseId, id) for id in range(1,9)]
    
    def printTxt(self):
        print "Case "+str(self.caseId)
        
                 

                