import time, cv2
import keyboard
from threading import Thread
from djitellopy import Tello
import numpy as np
from field_move import Field
from data import *

tello = Field(472, 170, 200, (180, 116, 0), (231, 116, 20), HAZARD_LIST)
tello.connect()
tello.streamon()


global img
running = True

# Video
def video():
    while running:
        img = tello.get_frame_read().frame
        img = cv2.resize(img, (360, 240))
        cv2.imshow("Video Feed", img)
        cv2.putText(img, f'Battery: {tello.get_battery()}% | Position: {tello.get_pos()}', (10,500), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1, 2)
        cv2.waitKey(1)
        
# Input
def tello_input():
    while running:
        if keyboard.is_pressed('space'):
            tello.emergency()
            print('Emergency stop')
            time.sleep(2)
        if keyboard.is_pressed('q'):
            exit()
            
# Create and run threads for input and video
video_feed = Thread(target=video)
input_feed = Thread(target=tello_input)

video_feed.start()
input_feed.start()

print(f'Battery: {tello.get_battery()}%')

# Movement commands
tello.takeoff()
time.sleep(1)

tello.move_posS([
    (404, 125, 106), # Move to top of highest building on right
    ((424, 85, 90), ('x', 'y', 'z')), # Move to scanning position
])
tello.rotate_clockwise(180)

print('scan')

tello.move_pos(
    (424, 85, 90) # Move to top of highest building on right
)
tello.land_pad()


running = False
video_feed.join()
input_feed.join()