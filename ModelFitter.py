import Shape
import Point
import math
import numpy as np
import AlignmentUtils
import Util
import cv2
from matplotlib import pyplot as plt

class ModelFitter:
    
    def __init__(self, asm, image):
        self.image = image
        self.gradientImage = self.generateGradientImage()
        plt.subplot(111),plt.imshow(self.gradientImage,cmap = 'gray')
        plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
        plt.show()
        self.asm = asm
        self.shape = Shape.Shape.fromVector(asm.mean)
        self.initialPlacement()
        
    def initialPlacement(self):
        angle = 90
        rot_matrix = np.array([[np.cos(angle), np.sin(angle)], [-np.sin(angle), np.cos(angle)]])
        for ind in range(len(self.shape.points)):
            c = np.array([self.shape.points[ind].x, self.shape.points[ind].y])
            c = c.dot(rot_matrix)
            self.shape.points[ind].x = c[0]
            self.shape.points[ind].y = c[1]
        for p in range(len(self.shape.points)):
            self.shape.points[p].x = self.shape.points[p].x+1500
            self.shape.points[p].y = self.shape.points[p].y+700
        
    def clahe(self, image, clipLimit=2.0, gridSize=(32,32)):
        cl = cv2.createCLAHE(clipLimit, gridSize)
        return cl.apply(image)
    
    def threshold(self, img, threshold):
        b = np.empty(img.shape)
        (h,w) = img.shape
        for i in range(h):
            for j in range(w):
                b[i,j] = 1 if img[i,j] > threshold else 0
        return b
        
    def generateGradientImage(self):
        #preprocess
        i = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        i = self.clahe(i)
        #use sobel to get edges
        sobelx = cv2.Sobel(i, cv2.CV_64F, 1, 0, ksize=9)
        sobely = cv2.Sobel(i, cv2.CV_64F, 0, 1, ksize=9)
        sobel = np.sqrt(sobelx**2 + sobely**2)
        #return self.threshold(sobel, 200000)
        return sobel
        
        
    def iterate(self):
        # new shape = max points along normal of current shape
        s = Shape.Shape([])
        for i, pt in enumerate(self.shape.points):
            s.addPoint(self.getMaxAlongNormal(i))
    
        variance = AlignmentUtils.alignToShape(s, Shape.Shape.fromVector(self.asm.mean), self.asm.w).getVector() - self.asm.mean
        newShape = self.asm.mean
        for i in range(len(self.asm.eigenvectors)):
            b = np.dot(self.asm.eigenvectors.T[:,i],variance)
            maxB = 3*math.sqrt(self.asm.eigenvalues[i])
            b = max(min(b, maxB), -maxB)
            newShape = newShape + self.asm.eigenvectors.T[:,i]*b

        self.shape = AlignmentUtils.alignToShape(Shape.Shape.fromVector(newShape), s, self.asm.w)
        
    #gets point with max edge response along normal to point
    def getMaxAlongNormal(self, pIdx):
        normal = self.shape.getNormalToPoint(pIdx)
        p = self.shape.points[pIdx]
    
        (ih, iw, c) = self.image.shape
        #find extremes of normal in image
        minR = -p.x / normal[0]
        if p.y + minR*normal[1] < 0:
            minR = -p.y / normal[1]
        elif p.y + minR*normal[1] > ih:
            minR = (ih - p.y) / normal[1]
        maxR = (iw - p.x) / normal[0]
        if p.y + maxR*normal[1] < 0:
            maxR = -p.y / normal[1]
        elif p.y + maxR*normal[1] > iw:
            maxR = (iw - p.y) / normal[1]
    
        tmp = maxR
        maxR = max(minR, maxR)
        minR = min(minR, tmp)
    
        img = self.image.copy()
        
        
        cv2.circle(img, \
            (int(normal[0]*minR + p.x), int(normal[1]*minR + p.y)), \
            5, (0, 0, 0))
        cv2.circle(img, \
            (int(normal[0]*maxR + p.x), int(normal[1]*maxR + p.y)), \
            5, (0, 0, 0))
        
        max_pt = p
        max_edge = 0        
        
        search = 50
        for side in range(-3, 3):
            new_p = Point.Point(p.x + side*-normal[1], p.y + side*normal[0])
            for t in Util.drange(-search if -search > minR else minR, \
                            search if search < maxR else maxR , .5):
        
                x = int(normal[0]*t + new_p.x)
                y = int(normal[1]*t + new_p.y)
                if x < 0 or x > iw or y < 0 or y > ih:
                    continue
                cv2.circle(img, (x, y), 3, (100,100,100))
                if self.gradientImage[y-1, x-1] > max_edge:
                    max_edge = self.gradientImage[y-1, x-1]
                    max_pt = Point.Point(new_p.x + t*normal[0], new_p.y + t*normal[1])
    
        for point in self.shape.points:
          cv2.circle(img, (int(point.x), int(point.y)), 3, (255,255,255))
        cv2.circle(img, (int(max_pt.x), int(max_pt.y)), 3, (255,255,255))
        cv2.namedWindow("Scale", cv2.WINDOW_NORMAL)
        cv2.imshow("Scale",img)
        cv2.waitKey(0)
        return max_pt    
        
    def visualize(self):
        cv2.namedWindow('Incisor Segmentation', cv2.WINDOW_NORMAL)
        i = np.asarray(self.image[:,:]).copy()
        for pIdx, p in enumerate(self.shape.points):
            cv2.circle(i, (int(p.x.real), int(p.y.real)), 2, (255,0,0), -1)
        cv2.imshow('Incisor Segmentation', i)
        cv2.waitKey(0)