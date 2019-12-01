import features 
import cv2
import numpy as np
import matplotlib.pyplot as plt

im1 = cv2.imread('output/000045.png')

template = cv2.imread('output/template.png')

template = cv2.cvtColor(template, cv2.COLOR_BGR2RGB)
im1 = im1[im1.shape[0]-720:,im1.shape[1]-720:,:]
template = template[50:350,50:350,:]
print(template.shape,im1.shape)
tmp = features.hog(template)

img = features.hog(im1)

print(img.shape,tmp.shape)
r,c,_ = tmp.shape
sse = np.zeros(img.shape[:2])
# print
for i in range(img.shape[0]-r):
    for j in range(img.shape[1]-c):
        sse[i,j] = np.sqrt(np.square(img[i:i+r,j:j+c,:] - tmp).sum(axis=(0,1))).sum()

tgt = np.argmin(sse[:img.shape[0]-r,:img.shape[1]-c])
match = np.unravel_index(tgt, (img.shape[0]-r,img.shape[1]-c))
print(match)
a = plt.figure()
ax = a.add_subplot(121)
plt.imshow(sse[:img.shape[0]-r,:img.shape[1]-c],cmap='gray')
ax = a.add_subplot(122)
plt.imshow(im1)
plt.show()
# print('best match position:',match)
# print('best candidate distance:',scores.min())
# a = plt.figure()
# ax = a.add_subplot(131)
# plt.imshow(im1)
# rect = plt.Rectangle(( match[1],match[0]),c,r, color='r', alpha=0.4)
# ax.add_patch(rect)

# a.add_subplot(132)
# plt.imshow(im1[match[0]:match[0]+r, match[1]:match[1]+c])
# plt.title('Problem 1 Result')