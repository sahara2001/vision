import features 
import cv2
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
import datetime 

im1 = cv2.imread('output/000045.png')

template = cv2.imread('output/template.png')

template = cv2.cvtColor(template, cv2.COLOR_BGR2RGB)

im1 = cv2.imread('without_Color.png')
im1 =  cv2.cvtColor(im1, cv2.COLOR_BGR2RGB)
template = cv2.imread('output/template.png')

template = cv2.cvtColor(template, cv2.COLOR_BGR2RGB)

ub = [[[255, 230, 200]]]
lb = [[[137,85,63]]]
x = ((im1 < ub).sum(axis=2) == 3 )*((im1 > lb).sum(axis=2) == 3 )
x = x.astype(np.int32)
a = plt.figure()
a.add_subplot(121)
plt.imshow(im1)
a.add_subplot(122)
plt.imshow(x,cmap='gray')
plt.show()

start = datetime.datetime.now()
# hsl test
im2 = cv2.cvtColor(im1, cv2.COLOR_RGB2HSV)




ub = [[[26, 150,256]]]
lb = [[[3,80,-1]]]
x = ((im2 < ub).sum(axis=2) == 3 )*((im2 > lb).sum(axis=2) == 3 )

x = x.astype(np.int)



print((datetime.datetime.now()-start).total_seconds())
a = plt.figure()
a.add_subplot(121)
plt.imshow(im2,cmap=cm.hsv)
a.add_subplot(122)
plt.imshow(x,cmap='gray')
plt.show()