
import cv2
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
import datetime 

color_image = cv2.imread('out/color000020.png')
color_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
# print(im1.shape)
# plt.imshow(im1,cmap='gray')
# plt.show()

cv2.circle(color_image,(100,100),1,(0,0,255))
cv2.imshow("IM", color_image)

cv2.waitKey(0)
