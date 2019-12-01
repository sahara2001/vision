import cv2
import numpy as np
import matplotlib.pyplot as plt
import datetime

im1 = cv2.imread('../output/000045.png')

template = cv2.imread('../output/template.png')

template = cv2.cvtColor(template, cv2.COLOR_BGR2RGB)

winSize = (64,64)
blockSize = (16,16)
blockStride = (8,8)
cellSize = (8,8)
nbins = 9
derivAperture = 1
winSigma = 4
histogramNormType = 0
L2HysThreshold = 2.0000000000000001e-01
gammaCorrection = 0
nlevels = 64

hog = cv2.HOGDescriptor(winSize,blockSize,blockStride,cellSize,nbins,derivAperture,winSigma,
                        histogramNormType,L2HysThreshold,gammaCorrection,nlevels)

#img = hog.compute(im1)
#tmp = hog.compute(im1[::2,::2,:])
#print(img.shape,tmp.shape)

winStride = (4,4)
padding = (8,8)
locations = ((20,20),)

#hist = hog.compute(im1[::2,::2,:],winStride,padding,locations)


meanShift = True
patch = (350,850)
# padding = (100,100)
template = im1[290:450,750:950,:]
print(template.shape)
locations = (patch,)
#hist = hog.compute(im1,winStride,padding,locations)
print(1)
# print(cv2.HOGDescriptor_getDefaultPeopleDetector().shape)
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
r,c,_ = template.shape
#im1 = im1[800:1000,250:350,:]
sse = np.zeros(im1.shape[:2])
print(1.5)
start = datetime.datetime.now()
(rects, weights) = hog.detectMultiScale(im1, winStride=winStride,padding=padding,scale=1.5, useMeanshiftGrouping=meanShift)
print(2)
print(rects)
for (x,y,w,h) in rects:
    cv2.rectangle(im1,(x,y), (x+w, y+h), (0,255,0), 2)


# print
# print(im1.shape)
# w= 800
# h = 250
# for i in range(0,200,10):
#     for j in range(0,200,10):
#         locations = ((h+i,w+j),)
#         desc = hog.compute(im1,winStride,padding,locations)
#         sse[i,j] = np.sqrt(np.square(desc - hist).sum(axis=(0,1))).sum()

# print(np.unravel_index(np.argmin(sse),template.shape[:2]))
print((datetime.datetime.now()-start).total_seconds())
a = plt.figure()
a.add_subplot(121)
plt.imshow(im1)
a.add_subplot(122)
plt.imshow(template,cmap='gray')
plt.show()