import cv2

img1 = cv2.imread('out/result000034.png')
# img2 = cv2.imread('2.jpg')
# img3 = cv2.imread('3.jpg')

height , width , layers =  img1.shape

video = cv2.VideoWriter('video.avi',-1,1,(width,height))
video.write(img1)

# im = []
for i in range(39,200,5):
    im = cv2.imread('out/result' +  str(i).zfill(6) + ".png")
    video.write(im)


cv2.destroyAllWindows()
video.release()