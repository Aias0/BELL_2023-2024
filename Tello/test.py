import cv2, time, keyboard
import numpy as np
from djitellopy import Tello
from vpython import *



tello = Tello()
tello.connect()

tello.takeoff()

# Remember to measure varation in distance
time.sleep(1)
tello.flip('r')
time.sleep(1)
tello.flip('f')
time.sleep(1)
tello.flip('l')
time.sleep(1)
tello.flip('b')