from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
# import the necessary packages
import argparse
import datetime
import imutils
import cv2

if __name__ == "__main__":
    # construct the argument parse and parse the arguments
    # ap = argparse.ArgumentParser()
    # ap.add_argument("-i", "--image", required=True,
    #                 help="path to the input image")
    # ap.add_argument("-w", "--win-stride", type=str, default="(8, 8)",
    #                 help="window stride")
    # ap.add_argument("-p", "--padding", type=str, default="(16, 16)",
    #                 help="object padding")
    # ap.add_argument("-s", "--scale", type=float, default=1.05,
    #                 help="image pyramid scale")
    # ap.add_argument("-m", "--mean-shift", type=int, default=-1,
    #                 help="whether or not mean shift grouping should be used")
    # args = vars(ap.parse_args())

    # evaluate the command line arguments (using the eval function like
    # this is not good form, but let's tolerate it for the example)
    # winStride = eval(args["win_stride"])
    # padding = eval(args["padding"])
    meanShift = True

    # initialize the HOG descriptor/person detector
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    # load the image and resize it
    image = cv2.imread('../output/jack2.jpg')
    image = imutils.resize(image, width=min(400, image.shape[1]))

    # detect people in the image
    start = datetime.datetime.now()
    (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4),
                                            padding=(8,8), scale=1.03, useMeanshiftGrouping=meanShift)
    print("[INFO] detection took: {}s".format(
        (datetime.datetime.now() - start).total_seconds()))

    # draw the original bounding boxes
    print(len(rects))
    for (x, y, w, h) in rects:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # show the output image
    cv2.imshow("Detections", image)
    cv2.waitKey(0)


    # print(img.shape)
    # # img = img[::4,::4,:]
    # # template = template[::4,::4,:]
    # result = match(img, template)
    #
    # candidates = np.argsort(result, axis=None)
    # k_match = candidates[-1]  # k top result
    # # print(k_match.shape)
    # r1, c1, _ = template.shape
    # k_match = np.unravel_index(k_match, (img.shape[0] - r1 + 1, img.shape[1] - c1 + 1))
    # print(k_match)
    # # ax = figs.add_subplot(1,len(K)+1,k+2)
    # # ax.title.set_text('k={}'.format(K[k]))
    # plt.imshow(img[k_match[0]:k_match[0] + r1, k_match[1]:k_match[1] + c1, :])
    # plt.show()
