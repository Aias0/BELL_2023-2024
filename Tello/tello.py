import time, cv2
import keyboard
from threading import Thread
from djitellopy import Tello
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
        cv2.imshow("Image", img)
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
Thread(target=video).start()
Thread(target=tello_input).start()

print(f'Battery: {tello.get_battery()}%')

# Movement commands
tello.takeoff()
time.sleep(1)
tello.move_up(100) #Set to 202 for compititon
tello.move_forward(500)
tello.move_forward(120)
tello.rotate_clockwise(180)
tello.move_down(20)
tello.move_left(178)
time.sleep(1)
print('scan')
tello.move_right(178)
tello.move_up(20)
tello.move_forward(490)
tello.land()

running = False