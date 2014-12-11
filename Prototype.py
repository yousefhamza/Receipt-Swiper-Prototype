__author__ = 'yousefhamza'

import cv2
import numpy as np

init_x = 0
init_y = 0
height = 50
width = 0
def getSwipedArea(event, x, y, flags, param):
    global init_x, init_y, height, width
    if event == cv2.EVENT_LBUTTONDOWN:
        init_x = x - 20
        init_y = y - 20
    elif event == cv2.EVENT_LBUTTONUP:
        cv2.destroyWindow('cropped line')
        width = x - init_x
        line = small_receipt[init_y:height+init_y, init_x:width+init_x]
        cv2.imshow('cropped line', line)

receipt = cv2.imread('Images/receipt0.jpg')

#resizing
if len(receipt) > 1000:
    small_receipt = cv2.resize(receipt,(0, 0), fx = 0.25, fy = 0.25)
else:
    small_receipt = receipt

cv2.imshow('first', small_receipt)
small_receipt = cv2.medianBlur(small_receipt, 3) #median filter
_,small_receipt = cv2.threshold(small_receipt, 127, 255, cv2.THRESH_BINARY) #thresholding


cv2.imshow('receipt', small_receipt)
cv2.setMouseCallback('receipt', getSwipedArea)
cv2.waitKey(0)

