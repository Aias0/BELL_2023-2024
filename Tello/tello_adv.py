import time, cv2, keyboard, logging
from djitellopy import Tello
from threading import Thread
import numpy as np
from bell_tello import Bell_Tello
from data import *
from support import *

tello = Bell_Tello((472, 170, 200), (180, 116, 0), (231, 116, 40), HAZARD_LIST)
tello.connect()
print(f'Battery: {tello.get_battery()}%')

global video
tello.streamon()
running = True

# Video
def CIC():
    first_run = True
    while running:
        # Video
        video = tello.get_frame_read().frame
        video = cv2.cvtColor(video, cv2.COLOR_BGR2RGB) 
        video = cv2.resize(video, (1440, 960))
        #Text Background
        text_bak = np.zeros_like(video, np.uint8)
        text_bak = cv2.rectangle(text_bak, (0, 910), (1440, 960), (255, 255, 255), -1)
        # Processing
        out = video.copy()
        alpha = 0.5
        mask = text_bak.astype(bool)
        out[mask] = cv2.addWeighted(video, alpha, text_bak, alpha - 0.75, 20)[mask]
        #Text
        out = cv2.putText(out, f'Batt: {tello.get_battery()}% | Pos: ({int(tello.get_pos()[0])}, {int(tello.get_pos()[1])}, {int(tello.get_pos()[2])}) | Dir: {tello.get_direction()[1]} - {tello.get_direction()[0]} | Temp: {tello.get_temperature()} / {tello.get_highest_temperature()}', 
                          (10,945), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1, 2)
        #Display
        cv2.imshow('Video Feed', out)
        if first_run: cv2.moveWindow('Video Feed', 10, 10)
        cv2.waitKey(1)
        
        # Input
        if keyboard.is_pressed('space'):
            tello.emergency()
            print('Emergency stop')
            time.sleep(2)
        elif keyboard.is_pressed('q'):
            tello.streamoff()
            tello.close_graph()
            exit()
        # Info
        if tello.get_battery() < 5:
            logging.critical(f'Battery dangerously low. {tello.get_battery}%')
        elif tello.get_battery() < 10:
            logging.warning(f'Battery low. {tello.get_battery}%')
        
# Create and run threads for input and video
CIC_feed = Thread(target=CIC)
CIC_feed.daemon(True)
CIC_feed.start()

# Movement commands
tello.takeoff()
time.sleep(2)
 
tello.move_pos_line(
    (404, 120, 120), # Move to top of highest building on right
)
time.sleep(2)
tello.move_pos_line(
    (424, 85, 90), # Move to scanning position
)
tello.rotate_clockwise(180)

print('scan')
tower_scan = tello.get_frame_read().frame
tower_scan = cv2.cvtColor(tower_scan, cv2.COLOR_RGB2BGR) 
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