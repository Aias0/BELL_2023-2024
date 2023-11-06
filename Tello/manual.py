from djitellopy import Tello
from threading import Thread
import numpy as np
import cv2, keyboard, time, logging, sys
from bell_tello import Bell_Tello
from data import *

tello = Bell_Tello((472, 170, 200), (180, 116, 0), (231, 116, 40), HAZARD_LIST)
tello.connect()
print(f'Battery: {tello.get_battery()}%')

tello.streamon()
running = True

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
        if keyboard.is_pressed('y'):
            tello.emergency()
            print('Emergency stop')
            time.sleep(2)
        if keyboard.is_pressed('u'):
            tello.streamoff()
            #tello.close_graph()
            exit()
        if keyboard.is_pressed('tab'):
            tello.toggle_video_direction()
        # Info
        if tello.get_battery() < 5:
            logging.critical(f'Battery dangerously low. {tello.get_battery()}%')
            time.sleep(1)
        elif tello.get_battery() < 10:
            logging.warning(f'Battery low. {tello.get_battery()}%')
            time.sleep(1)
        first_run = False
        
# Create and run threads for input and video
CIC_feed = Thread(target=CIC)
CIC_feed.start()

tello.takeoff()
time.sleep(2)
tello.land()
go = False
while not go:
    if keyboard.is_pressed('w'):
        go = True
else:
    tello.takeoff()
    tello.move(231, 50, 50)
    time.sleep(1)
    tello.land()