import time, cv2, keyboard, logging
from djitellopy import Tello
from threading import Thread
import numpy as np
from bell_tello import Bell_Tello
from data import *

tello = Bell_Tello(472, 170, 200, (180, 116, 0), (231, 116, 20), HAZARD_LIST)
#tello = Tello()
tello.connect()



global img
tello.streamon()
running = True

# Video
def video():
    while running:
        img = tello.get_frame_read().frame
        img = cv2.resize(img, (360, 240))
        cv2.imshow("Video Feed", img)
        cv2.waitKey(1)
        #cv2.putText(img, f'Batt: {tello.get_battery()}% | Pos: {tello.get_pos()} | Dir: {tello.get_direction()[1]} | {tello.get_direction()[0]} | Temp: {tello.get_temperature} / {tello.get_highest_temperature}', (10,500), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1, 2)
        if keyboard.is_pressed('space'):
            tello.emergency()
            print('Emergency stop')
            time.sleep(2)
        if tello.get_battery < 5:
            logging.critical(f'Battery dangerously low. {tello.get_battery}%')
        elif tello.get_battery < 10:
            logging.warning(f'Battery low. {tello.get_battery}%')
        
            
# Create and run threads for input and video
video_feed = Thread(target=video)
video_feed.start()

print(f'Battery: {tello.get_battery()}%')

# Movement commands
tello.takeoff()
time.sleep(1)

tello.move_pos_line_mult([
    (404, 125, 106), # Move to top of highest building on right
    (424, 85, 90), # Move to scanning position
])
tello.rotate_clockwise(180)

print('scan')

tello.move_pos_line(
    (424, 85, 90), # Move to top of highest building on right
)

tello.land_pad()


running = False
video_feed.join()
tello.streamoff()