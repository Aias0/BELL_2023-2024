import cv2, time
import numpy as np
from scipy import ndimage

test_imgs = ["C:/Users/quent/OneDrive/Desktop/unnamed.png", "C:/Users/quent/OneDrive/Desktop/fnp-toc-default-thermal-imaging.jpg", "C:/Users/quent/OneDrive/Desktop/thermal-hot-spot-300x224.jpg", "C:/Users/quent/OneDrive/Desktop/HotSpot-thermal-image.jpg", "C:/Users/quent/OneDrive/Desktop/eyJidWNrZXQiOiJ3ZXZvbHZlci1wcm9qZWN0LWltYWdlcyIsImtleSI6ImZyb2FsYS8xNjI5ODg4Nzk4MzYzLWNpcmN1aXQtcGFuZWwtMi5qcGciLCJlZGl0cyI6eyJyZXNpemUiOnsid2lkdGgiOjk1MCwiZml0IjoiY292ZXIifX19.webp"]

thermal_image = cv2.imread(test_imgs[0])
thermal_image = cv2.resize(thermal_image, (720, 480))
cv2.imshow('Input', cv2.resize(thermal_image, (720, 480)))
#thermal_image = np.asarray(self.thermal_pixel_matrix, dtype=np.uint8)
lowerb = np.array([0, 0, 230], np.uint8)
upperb = np.array([255, 255, 255], np.uint8)
frame = cv2.inRange(thermal_image, lowerb, upperb)
blobs = frame > 100
labels, nlabels = ndimage.label(blobs)
# find the center of mass of each label
t = ndimage.center_of_mass(frame, labels, np.arange(nlabels) + 1 )
# calc sum of each label, this gives the number of pixels belonging to the blob
s  = ndimage.sum(blobs, labels,  np.arange(nlabels) + 1 )
# print the center of mass of the largest blob
center_of_mass = [int(x) for x in t[s.argmax()][::-1]]
print(center_of_mass) # notation of output (y,x)
targeting_img =  cv2.cvtColor(frame,cv2.COLOR_GRAY2RGB)
targeting_img = cv2.circle(targeting_img, center_of_mass, radius=4, color=(0, 0, 255), thickness=-1)
cv2.imshow('Mask', targeting_img)
cv2.waitKey()

# Lazer to Camera 28.541
#Axis to camera 21.072degrees, 40.212, distnace 14.458, long 37.523