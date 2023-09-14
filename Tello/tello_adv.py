import time, cv2, keyboard, logging
from djitellopy import Tello
from threading import Thread
import numpy as np
from bell_tello import Bell_Tello
from data import *

tello = Bell_Tello(472, 170, 200, (180, 116, 0), (231, 116, 40), HAZARD_LIST)
Tello()
tello.connect()



global img
tello.streamon()
running = True

# Video
def CIC():
    while running:
        # Video
        img = tello.get_frame_read().frame
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
        img = cv2.resize(img, (360*4, 240*4))
        cv2.putText(img, f'Batt: {tello.get_battery()}% | Pos: {tello.get_pos()} | Dir: {tello.get_direction()[1]} | {tello.get_direction()[0]} | Temp: {tello.get_temperature} / {tello.get_highest_temperature}', (10,500), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1, 2)
        cv2.imshow("Video Feed", img)
        cv2.waitKey(1)
        # Input
        if keyboard.is_pressed('space'):
            tello.emergency()
            print('Emergency stop')
            time.sleep(2)
        elif keyboard.is_pressed('q'):
            exit()
        # Info
        if tello.get_battery() < 5:
            logging.critical(f'Battery dangerously low. {tello.get_battery}%')
        elif tello.get_battery() < 10:
            logging.warning(f'Battery low. {tello.get_battery}%')
        
            
# Create and run threads for input and video
CIC_feed = Thread(target=CIC)
CIC_feed.start()

print(f'Battery: {tello.get_battery()}%')

# Movement commands
tello.takeoff()
time.sleep(100)
 
tello.move_pos_line_mult([
    (404, 120, 120), # Move to top of highest building on right
    (424, 85, 90), # Move to scanning position
])
tello.rotate_clockwise(180)

print('scan')
tower_scan = tello.get_frame_read().frame
cv2.cvtColor(tower_scan, cv2.COLOR_RGB2BGR) 
tower_color = cv2.resize(tower_scan, (360, 240))
winname = cv2.namedWindow('Tower Color')
cv2.moveWindow(winname, 40,30)
cv2.imshow(winname, tower_scan)
time.sleep(2)

tello.rotate_counter_clockwise(180)

tello.land_pad()

# Closeing threads
running = False
CIC_feed.join()
tello.streamoff()
tello.close_graph()