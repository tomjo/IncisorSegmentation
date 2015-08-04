'''
Different algorithms for pre-processing the dental radiographs
'''
import cv2
import numpy as np
from matplotlib import pyplot as plt

#hat
def tophat(image):
    image_top = white_tophat_transform(image)
    image_bottom = black_tophat_transform(image)

    image = cv2.add(image, image_top)
    image = cv2.subtract(image, image_bottom)
    return image

#top-hat transform
#http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html
def white_tophat_transform(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_TOPHAT, kernel)

def black_tophat_transform(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_BLACKHAT, kernel)

#fourier
#http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_transforms/py_fourier_transform/py_fourier_transform.html
#http://www.bogotobogo.com/python/OpenCV_Python/python_opencv3_Image_Fourier_Transform_FFT_DFT.php
def fourier(image):
    img_float32 = np.float32(image)

    dft = cv2.dft(img_float32, flags = cv2.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)
    
    rows, cols = image.shape
    crow, ccol = rows/2 , cols/2     # center
    
    # create a mask first, center square is 1, remaining all zeros
    mask = np.zeros((rows, cols, 2), np.uint8)
    mask[crow-30:crow+30, ccol-30:ccol+30] = 1
    
    # apply mask and inverse DFT
    fshift = dft_shift*mask
    f_ishift = np.fft.ifftshift(fshift)
    img_back = cv2.idft(f_ishift)
    img_back = cv2.magnitude(img_back[:,:,0],img_back[:,:,1])
    
    return img_back
   
    
#gaussian smoothing filter
#http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_filtering/py_filtering.html
def gaussian(image):
    return cv2.GaussianBlur(image,(5,5),0)
    
#median filtering
#histogram equalization
def medianAndHistogram(image):
    return histogram(median(image))
    
#http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_filtering/py_filtering.html
def median(image):
    return cv2.medianBlur(image,5)

#http://docs.opencv.org/master/d5/daf/tutorial_py_histogram_equalization.html
def histogram(image):
    return cv2.equalizeHist(image)
    
#https://en.wikipedia.org/wiki/Adaptive_histogram_equalization
def clahe(image, clipLimit=2.0, gridSize=(32,32)):
    cl = cv2.createCLAHE(clipLimit, gridSize)
    return cl.apply(image)

#you can test the effects of the different algorithms here
def testalgorithms():
    img = cv2.imread('Radiographs/01.tif', 0)
    img_tophat = tophat(img)
    #img_fourier = fourier(img) #does not work well
    img_gaussian = gaussian(img)
    img_medianhist = medianAndHistogram(img)
    img_clahe = clahe(img)

    #show images
    height = 500
    scale = height / float(img.shape[0])
    window_width = int(img.shape[1] * scale)
    window_height = int(img.shape[0] * scale)

    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('image', window_width, window_height)
    cv2.imshow('image',img)
    cv2.waitKey()
    cv2.imshow('image',img_tophat)
    cv2.waitKey()
    cv2.imshow('image',img_gaussian)
    cv2.waitKey()
    cv2.imshow('image',img_medianhist)
    cv2.waitKey()
    cv2.imshow('image',img_clahe)
    cv2.waitKey()