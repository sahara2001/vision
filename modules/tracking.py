import cv2
import matplotlib.pyplot as plt
import numpy as np
from numpy import ma
from scipy import integrate
from scipy import linalg

im1 = cv2.imread('../out/search.png')
im1 = cv2.cvtColor(im1, cv2.COLOR_BGR2RGB)
template = cv2.imread('../out/template1.png')
template = cv2.cvtColor(template, cv2.COLOR_BGR2RGB)

tmp_yc = np.tile(np.array(range(1,template.shape[0]+1)), (template.shape[1], 1)).transpose()
tmp_xr= np.tile(np.array(range(1,template.shape[1]+1)), (template.shape[0],1))
sample = np.concatenate( [tmp_xr[...,np.newaxis], tmp_yc[...,np.newaxis], template],axis=2)
cov_0 = np.cov(sample.reshape(-1,5).transpose(), bias=True)
# template = cv2.imread()
# im1 = cv2.imread('input/target.jpg')
# im2 = cv2.imread('input/img2.jpg')

# im1=cv2.cvtColor(im1, cv2.COLOR_BGR2RGB)
# im2=cv2.cvtColor(im2, cv2.COLOR_BGR2RGB)

idx_yc = np.tile(np.array(range(1,im1.shape[0]+1)), (im1.shape[1], 1)).transpose()
idx_xr= np.tile(np.array(range(1,im1.shape[1]+1)), (im1.shape[0],1))

# print(idx_yc)
# print(idx_xr)
# print(im1.shape)
# feature vector
X1 = np.concatenate( [idx_xr[...,np.newaxis], idx_yc[...,np.newaxis], im1],axis=2)
# X2 = np.concatenate( [idx_xr[...,np.newaxis], idx_yc[...,np.newaxis], im2],axis=2)

H, W, _ = im1.shape
r,c,_ = template.shape
mn = r*c

# similarity
scores = np.zeros((H-r, W-c))
step = 1

# assert im1.shape == im2.shape 
# complete covariance matching using 
for i in range(0, H-r, step):
    for j in range(0,W-c, step):
        ## TODO: compute cov
        sample = X1[i:i+r,j:j+c]
        # print(sample.shape)
        cov = np.cov(sample.reshape(-1,5).transpose(), bias=True) #/ mn 
        # print(cov_0.shape)
        # print(cov.shape)
        l,_ = linalg.eig(cov_0,cov)
        assert np.sum(l==0) == 0
        scores[i,j] = np.sqrt(np.sum(np.square(ma.log(l).filled(0))))   #use masked array for log

assert np.sum(scores==0) ==0
match  = np.unravel_index(scores.argmin() , scores.shape)
print('best match position:',match)
print('best candidate distance:',scores.min())
a = plt.figure()
ax = a.add_subplot(131)
plt.imshow(im1)
rect = plt.Rectangle(( match[1],match[0]),c,r, color='r', alpha=0.4)
ax.add_patch(rect)

a.add_subplot(132)
plt.imshow(im1[match[0]:match[0]+r, match[1]:match[1]+c])
plt.title('Problem 1 Result')

a.add_subplot(132)
plt.imshow(scores)
plt.title('Match Distance')

#plt.savefig('output/problem_1_result.jpg')

plt.show()