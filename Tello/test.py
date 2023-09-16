import cv2, time
import numpy as np
from djitellopy import Tello

# This is a commnet

tello = Tello()

tello.connect()

tello.takeoff()
time.sleep(1)
tello.flip()
