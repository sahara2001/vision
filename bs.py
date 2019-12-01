import features 
import cv2
import numpy as np
import matplotlib.pyplot as plt

im1 = cv2.imread('output/000045.png')

template = cv2.imread('output/template.png')

template = cv2.cvtColor(template, cv2.COLOR_BGR2RGB)

