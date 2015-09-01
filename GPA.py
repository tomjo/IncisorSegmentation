import numpy as np
import sys
import AlignmentUtils

#aligns set of shapes
def gpa(shapes, w):
    # rotate/scale/translate each shape to match first
    shapes[1:] = [AlignmentUtils.alignToShape(s, shapes[0], w) for s in shapes[1:]]
    a = shapes[0]
    trans = np.zeros((4, len(shapes)))

    accuracy = sys.maxint
    while True:
      mean = calcMeanShape(shapes)
      mean = AlignmentUtils.alignToShape(mean, a, w)
      for i in range(len(shapes)):
        trans[:, i] = AlignmentUtils.getPoseParams(shapes[i], mean, w)
        shapes[i] = AlignmentUtils.applyPoseParams(shapes[i], trans[:,i])

      # Stopcriteria: average transformation close to IDENTITY, als het verschil kleiner wordt -> precisie limiet bereikt
      diff = np.mean(np.array([1, 0, 0, 0]) - np.mean(trans, axis=1))**2
      if diff > accuracy:
        break
      accuracy = diff
    return shapes
    
def calcMeanShape(shapes):
    mean = shapes[0]
    for shape in shapes[1:]:
        mean = mean + shape
    return mean / len(shapes)
