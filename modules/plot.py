import matplotlib.pyplot as plt
import cv2
import numpy as np
import time
im = cv2.imread("../output/hand.png")
im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
mean = np.zeros(3)
tik = time.time()
for color in range(3):
    count = 0
    for r in range(im.shape[0]):
        for c in range(im.shape[1]):
            if im[r,c,color] > 0:
                mean[color] += im[r,c,color]
                count += 1
    mean[color] /= count
    count = 0
tok = time.time()
print(mean)
print(tok-tik)
plt.imshow(im)
plt.show()