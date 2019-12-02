
import cv2
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
import datetime 

ub = [[[15, 220,256]]]
lb = [[[3,90,-1]]]
kernel = np.ones((4,4),dtype=uint8)
T = 10

    # x = cv2.dilate(x,kernel,iterations = 1)
    
def getHand(img, ub, lb):
    img = cv2.GaussianBlur(img,(5,5),0)
    im2 = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    x = ((im2 < ub).sum(axis=2) == 3 )*((im2 > lb).sum(axis=2) == 3)

    
    x = x.astype(np.uint8)
    # x = cv2.morphologyEx(x,cv2.MORPH_CLOSE, kernel)
    x = cv2.morphologyEx(x,cv2.MORPH_OPEN, kernel)
    x = cv2.medianBlur(x, 5)
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

def getFingerTip1(x,depth):

    row, col = np.where(x>0)
    depth = depth * x
    # mrow = np.mean(row)
    # mcol = np.mean(col)
    # stdrow = np.std(row)
    # stdcol = np.std(col)
    # print(mrow,mcol,stdrow,stdcol)
    # depth_sub = depth[int(mrow-3*stdrow):int(mrow+3*stdrow), int(mcol-3*stdcol):int(mcol+3*stdcol)]


    ma = np.argmin(depth + (depth< T)*255)
    print(np.min(depth + (depth<T)*255))
    ma = np.unravel_index(ma,depth.shape)
    # ma = (ma[0] + int(mrow - 1 * stdrow), ma[1] + int(mcol - 1 * stdcol))
    return ma


if __name__ == '__main__':

    im1 = cv2.imread('output/000045.png')

    template = cv2.imread('output/template.png')

    template = cv2.cvtColor(template, cv2.COLOR_BGR2RGB)

    im1 = cv2.imread('out/color000030.png')
    depth = cv2.imread('out/depth000050.png')
    # im1 =  cv2.cvtColor(im1, cv2.COLOR_BGR2RGB)
    template = cv2.imread('output/template.png')

    template = cv2.cvtColor(template, cv2.COLOR_BGR2RGB)

    ub = [[[255, 255, 200]]]
    lb = [[[137,85,63]]]
    x = ((im1 < ub).sum(axis=2) == 3 )*((im1 > lb).sum(axis=2) == 3 )
    x = x.astype(np.int32)
    # a = plt.figure()
    # a.add_subplot(121)
    # plt.imshow(im1)
    # a.add_subplot(122)
    # plt.imshow(x,cmap='gray')
    # plt.show()

    start = datetime.datetime.now()
    # hsl test
    im2 = cv2.cvtColor(im1, cv2.COLOR_RGB2HSV)




    ub = [[[26, 240,256]]]
    lb = [[[3,80,-1]]]
    x = ((im2 < ub).sum(axis=2) == 3 )*((im2 > lb).sum(axis=2) == 3 )

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
    a = plt.figure()
    a.add_subplot(121)
    plt.imshow(im2,cmap=cm.hsv)
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