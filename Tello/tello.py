import cv2, time
import keyboard
from threading import Thread
from djitellopy import Tello
from data import *

tello = Tello()
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


running = False
video_feed.join()
input_feed.join()