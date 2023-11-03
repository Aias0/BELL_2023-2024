import cv2, time, json, base64, scipy, statistics
import numpy as np
from scipy import ndimage
from scipy.interpolate import interp1d
from bell.avr.mqtt.payloads import AvrThermalReadingPayload

target_range = (23, 40)

test_imgs = ['Misc/Thermal_Images/unnamed.png', "Misc/Thermal_Images/fnp-toc-default-thermal-imaging.jpg", "Misc/Thermal_Images/thermal-hot-spot-300x224.jpg", "Misc/Thermal_Images/HotSpot-thermal-image.jpg", "Misc/Thermal_Images/eyJidWNrZXQiOiJ3ZXZvbHZlci1wcm9qZWN0LWltYWdlcyIsImtleSI6ImZyb2FsYS8xNjI5ODg4Nzk4MzYzLWNpcmN1aXQtcGFuZWwtMi5qcGciLCJlZGl0cyI6eyJyZXNpemUiOnsid2lkdGgiOjk1MCwiZml0IjoiY292ZXIifX19.webp"]

payload = AvrThermalReadingPayload(data= 'FBUWFhYVFhUUFhYZGBYVFRQVFhcaGBUUFRUWGCAaFxYUFRYXGhgWFRQVFRYXFhUUExQUFhYWFRQTExQVFRQUEw==')
#payload = {"data": "FBYWFxYWFhYUFhcaGBcWFhUWFxgaGBYWFRYWGSEaFxYVFhYXHBgWFxUWFhYYFxYWFBUWFhYWFRQUFBUVFhQVFA=="}

#data = json.loads(payload)["data"]
data = payload['data']
# decode the payload
base64Decoded = data.encode("utf-8")
asbytes = base64.b64decode(base64Decoded)
pixel_ints = list(bytearray(asbytes))
thermal_grid = [[0 for _ in range(8)] for _ in range(8)]
k = 0
for i in range(len(thermal_grid)):
    for j in range(len(thermal_grid[0])):
        thermal_grid[i][j] = pixel_ints[k]
        k+=1
img = np.array(thermal_grid)
lowerb = np.array(target_range[0], np.uint8)
upperb = np.array(target_range[1], np.uint8)
mask = cv2.inRange(img, lowerb, upperb)
#mask = np.zeros((8, 8))
print(mask)
if np.all(np.array(mask) == 0):
    exit()
blobs = mask > 100
labels, nlabels = ndimage.label(blobs)
# find the center of mass of each label
t = ndimage.center_of_mass(mask, labels, np.arange(nlabels) + 1 )
# calc sum of each label, this gives the number of pixels belonging to the blob
s  = ndimage.sum(blobs, labels,  np.arange(nlabels) + 1 )
# print the center of mass of the largest blob
heat_center = [float(x) for x in t[s.argmax()][::-1]]
print(heat_center) # notation of output (y,x)
move_range = [20, -20]
m = interp1d([0, 8], move_range)
print(m(3))