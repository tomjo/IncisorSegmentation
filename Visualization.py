import numpy as np
import cv2
import math

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