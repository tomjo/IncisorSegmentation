import ASM
import ModelFitter
import Util

shapes = Util.loadLandmarks(1, excl=[1])
a = ASM.ASM(shapes)
i = Util.loadImage('01')
m = ModelFitter.ModelFitter(a, i)
m.visualize()
for i in range(1):
    m.iterate()   
m.visualize()