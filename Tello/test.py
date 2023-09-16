import cv2, time
import numpy as np
from djitellopy import Tello


tello = Tello()

tello.connect()

tello.takeoff()
time.sleep(1)
tello.flip()
