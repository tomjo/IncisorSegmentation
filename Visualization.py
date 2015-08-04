import numpy as np
import cv2
import math
from ASM import ASM
from Case import Case, Incisor
import Util
from VarianceModel import VarianceModel
import Preprocess_algorithms
    
def renderLandmarks(landmarks):
    minX = landmarks[:,1].min()
    maxX = landmarks[:,1].max()
    minY = landmarks[:,0].min()
    maxY = landmarks[:,0].max()
    
    img = np.zeros((int(maxY-minY)+1, int(maxX-minX)+1))
    
    for i in range(len(landmarks)):
        img[int(landmarks[i,0] - minY), int(landmarks[i,1] - minX)] = 1
        
    cv2.imshow('Landmarks', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def renderLandmarksOverImage(landmarks, img):
    tmp = img.copy();
    for i in range(len(landmarks)-1):
        cv2.line(tmp, (int(landmarks[i, 1]), int(landmarks[i,0])), (int(landmarks[i+1,1]), int(landmarks[i+1,0])), (0, 255, 0))
        
    scale = 800/float(img.shape[1])
    width = int(img.shape[1]*scale)
    height = int(img.shape[0]*scale)
    cv2.namedWindow('Landmarks over img', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Landmarks over img', width, height)
    cv2.imshow('Landmarks over img', tmp)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def calcMeanAndShow():
    asm = ASM(Util.getIncisorVectors(1))
    incisor = Incisor(None)
    incisor.readVector(asm.meanModel())
    renderLandmarks(incisor.lm)
    
def alignModel(incisor=1,render=True):
    asm = ASM(Util.getIncisorVectors(incisor))
    asm.align()
    asm.rescaleAndRealign()
    if render:
        renderLandmarks(asm.meanShape.lm)
    return asm
    
def alignModelAndVisualizeShapes():
    asm = alignModel()
    for shape in asm.lm:
        renderLandmarks(shape.lm)

def doPCA():
    asm = alignModel()
    varm = VarianceModel(asm)
    shapes = varm.fit(1,10)
    
    renderLandmarks(asm.meanShape.lm)
    incisor = Incisor(None)
    for i in range(len(shapes)):
        incisor.readVector(shapes[i, :])
        renderLandmarks(incisor.lm)

def draw():
    img = cv2.imread("Radiographs/01.tif", 0)
    #img = Preprocess_algorithms.clahe(img)
    for i in range(1,8):
        #asm = alignModel(i, False)
        #varm = VarianceModel(asm)
        #shapes = varm.fit(1,10)
        #incisor = Incisor(None)
        asm = ASM(Util.getIncisorVectors(i))
        #for i in range(len(shapes)):
        #    incisor.readVector(shapes[i, :])
        cv2.polylines(img, np.int32([asm.lm]), True, (0,255,0), 2)
    cv2.namedWindow("main",0)
    cv2.resizeWindow("main", 1500, 900)
    cv2.imshow("main", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    
    