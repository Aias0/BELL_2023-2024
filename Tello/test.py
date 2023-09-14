import cv2

img = cv2.imread('Misc\\tello_calibration_image.png')
img = cv2.resize(img, (1000, 750))
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
cv2.imshow('Test', img)

cv2.waitKey()