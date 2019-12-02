
import cv2

import numpy as np
import matplotlib.pyplot as plt
from pylab import *
import datetime 

ub = [[[15, 220,256]]]
lb = [[[3,100,-1]]]
kernel = np.ones((4,4),dtype=uint8)
T = 5
R = 10
R1=5

    # x = cv2.dilate(x,kernel,iterations = 1)
r_seq = [-3,-3,-2,-1,0,1,2,3,3,3,2,1,0,-1,-2,-3]
c_seq = [0,1,2,3,3,3,2,1,0,-1,-2,-3,-3,-3,-2,-1]
star = cv2.xfeatures2d.StarDetector_create()

def fast(img, R=3, pts=16, T=10, n=9, r_seq=r_seq, c_seq=c_seq):
    result = np.zeros(img.shape)
    for r in range(3,im2.shape[0]-3):
        for c in range(3,im2.shape[1]-3):
            # center pixel
            ref = img[r,c]
            prev = 0  # represent count and inequality
            # loop through circle, add n iteration to gurantee a solution
            for i in range(pts+n):
                idx = i % pts
                cur = img[r+r_seq[idx], c+c_seq[idx]]
                # use pos and neg sign to express greater or less than cases, abs value to express count
                if prev >= 0:
                    if  cur > ref+T:
                        prev+=1
                    elif cur < ref-T:
                        prev=-1
                    else:
                        prev=0
                elif prev <= 0:
                    if cur < ref-T:
                        prev-=1
                    elif cur > ref+T: 
                        prev=1
                    else:
                        prev=0
                
                if abs(prev) >= n:
                    result[r,c] = 1
    return result


def getHand(img, ub, lb,prev=None):
    img = cv2.GaussianBlur(img,(5,5),0)
    im2 = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    x = ((im2 < ub).sum(axis=2) == 3 )*((im2 > lb).sum(axis=2) == 3)

    
    x = x.astype(np.uint8)
    # x = cv2.morphologyEx(x,cv2.MORPH_CLOSE, kernel)
    x = cv2.morphologyEx(x,cv2.MORPH_OPEN, kernel)
    x = cv2.medianBlur(x, 5)
    if prev is not None:
        x[int(prev[0] - R):int(prev[0]+R),int(prev[1] - R):int(prev[1]+R)] = 1
    # x = cv2.medianBlur(x, 7)
    # x = cv2.medianBlur(x, 3)
    return x

def getFingerTip(x,depth):
    depth = cv2.GaussianBlur(depth,(5,5),0)
    row, col = np.where(x>0)
    mrow = np.mean(row)
    mcol = np.mean(col)
    stdrow = np.std(row)
    stdcol = np.std(col)
    # print(mrow,mcol,stdrow,stdcol)
    depth_sub = depth[int(mrow-3*stdrow):int(mrow+3*stdrow), int(mcol-3*stdcol):int(mcol+3*stdcol)]


    ma = np.argmin(depth_sub + (depth_sub < 1)*255)
    print(np.min(depth_sub + (depth_sub < 1)*255), 'd3pth')
    ma = np.unravel_index(ma,depth_sub.shape)
    ma = (ma[0] + int(mrow - 1 * stdrow), ma[1] + int(mcol - 1 * stdcol))
    return ma

def getFingerTip1(x,depth,prev=None):
    #depth = cv2.GaussianBlur(depth,(5,5),0)
    depth = cv2.medianBlur(depth, 3)
    # row, col = np.where(x>0)
    depth = depth * x
    if prev is not None:
        depth[int(prev[0] - R):int(prev[0]+R),int(prev[1] - R):int(prev[1]+R)] = 1
    # mrow = np.mean(row)
    # mcol = np.mean(col)
    # stdrow = np.std(row)
    # stdcol = np.std(col)
    # print(mrow,mcol,stdrow,stdcol)
    # depth_sub = depth[int(mrow-3*stdrow):int(mrow+3*stdrow), int(mcol-3*stdcol):int(mcol+3*stdcol)]
    
    ## require close to keypoints
    
    
    # kp = star.detect(depth)
    # pts = cv2.KeyPoint_convert(kp)
    
    # interest = 

    ma = np.argmin(depth + (depth < T)*255)
    print(np.min(depth + (depth < T)*255))
    ma = np.unravel_index(ma,depth.shape)
    # ma = (ma[0] + int(mrow - 1 * stdrow), ma[1] + int(mcol - 1 * stdcol))
    return ma


if __name__ == '__main__':

    im1 = cv2.imread('output/000045.png')

    template = cv2.imread('output/template.png')

    template = cv2.cvtColor(template, cv2.COLOR_BGR2RGB)

    im1 = cv2.imread('out/color000030.png')
    depth = cv2.imread('out/depth000030.png')
    im1 =  cv2.cvtColor(im1, cv2.COLOR_BGR2RGB)
    im1 = cv2.GaussianBlur(im1,(5,5),0)

    template = cv2.imread('output/template.png')

    template = cv2.cvtColor(template, cv2.COLOR_BGR2RGB)

    # ub = [[[255, 255, 200]]]
    # lb = [[[137,85,63]]]
    x = ((im1 < ub).sum(axis=2) == 3 )*((im1 > lb).sum(axis=2) == 3 )
    x = x.astype(np.int32)
    # a = plt.figure()
    # a.add_subplot(121)
    # plt.imshow(im1)
    # a.add_subplot(122)
    # plt.imshow(x,cmap='gray')
    # plt.show()
    # depth = cv2.GaussianBlur(depth,(5,5),0)
    
    start = datetime.datetime.now()
    # hsl test
    im2 = cv2.cvtColor(im1, cv2.COLOR_RGB2HSV)

    ## FAST
    print('FAST')
    # sift = cv2.xfeatures2d.SIFT_create()
    
    # fast = cv2.FastFeatureDetector_create(threshold=12)
    # kp = fast.detect(gray,None)
    
    # print(depth.max())
    # plt.imshow(depth,cmap='gray')
    # plt.show()
    # kp = sift.detect(depth,cv2.FAST_FEATURE_DETECTOR_TYPE_9_16)
    # print(kp)
    img2 = cv2.drawKeypoints(depth, kp, depth, color=(255,0,0))
    cv2.imshow('im',depth)
    cv2.waitKey(0)
    
    
    # print(kp)
    # plt.plot(kp)
    # plt.imshow(depth,cmap='gray')
    # plt.show()


    x = ((im2 < ub).sum(axis=2) == 3)*((im2 > lb).sum(axis=2) == 3 )

    x = x.astype(np.uint8)



    # print((datetime.datetime.now()-start).total_seconds())
    # a = plt.figure()
    # a.add_subplot(121)
    # plt.imshow(im2,cmap=cm.hsv)
    # a.add_subplot(122)
    # plt.imshow(x,cmap='gray')
    # plt.show()


    

    kernel = np.ones((16,16), np.uint8)
    kernel = np.ones((8,8), np.uint8)

    # x = cv2.dilate(x,kernel,iterations = 1)
    x = cv2.morphologyEx(x,cv2.MORPH_OPEN, kernel)
    x = cv2.medianBlur(x, 5)
    x = cv2.medianBlur(x, 7)
    x = cv2.medianBlur(x, 3)

    # x = cv2.dilate(x,kernel,iterations = 1)
    # kernel = np.ones((4,4), np.uint8)
    # x = cv2.morphologyEx(x,cv2.MORPH_OPEN, kernel)

    # x = cv2.morphologyEx(x,cv2.MORPH_CLOSE, kernel)
    # x = cv2.morphologyEx(x,cv2.MORPH_CLOSE, kernel)
    kernel = np.ones((8,8), np.uint8)

    row, col = np.where(x>0)
    mrow = np.mean(row)
    mcol = np.mean(col)
    stdrow = np.std(row)
    stdcol = np.std(col)
    print(mrow)
    print(mcol)
    print(stdrow)
    print(stdcol)
    # cv2.rectangle(im2, (mx-3*stdx, my-3*stdy), (mx+3*stdx, my+3*stdy), (0,255,0), 2)
    # cv2.imshow("IM",im2)
    # cv2.waitKey(0)
    # plt.imshow(im1)
    # plt.show()
    a = plt.figure()
    a.add_subplot(121)
    plt.imshow(im1)
    # plt.hsv()
    a.add_subplot(122)
    plt.imshow(x,cmap='gray')
    plt.show()

    depth_sub = depth[int(mrow-3*stdrow):int(mrow+3*stdrow), int(mcol-3*stdcol):int(mcol+3*stdcol), 0]


    ma = np.argmin(depth_sub + (depth_sub==0)*255)
    ma = np.unravel_index(ma,depth_sub.shape)
    ma = (ma[0] + int(mrow - 3 * stdrow), ma[1] + int(mcol - 3 * stdcol))
    print(ma)

    
    plt.imshow(im2)
    plt.show()