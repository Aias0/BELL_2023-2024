from bell_tello import Bell_Tello
from data import *
from djitellopy import Tello
from threading import Thread
import numpy as np
import cv2, keyboard, time, logging

tello = Tello()
tello.connect()

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
        out = cv2.putText(out, f'Batt: {tello.get_battery()}%', 
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
        if keyboard.is_pressed('q'):
            tello.streamoff()
            tello.close_graph()
            exit()
        if keyboard.is_pressed('1'):
            tello.set_video_direction(Tello.CAMERA_FORWARD)
        if keyboard.is_pressed('1'):
            tello.set_video_direction(Tello.CAMERA_DOWNWARD)
        # Info
        if tello.get_battery() < 5:
            logging.critical(f'Battery dangerously low. {tello.get_battery}%')
        elif tello.get_battery() < 10:
            logging.warning(f'Battery low. {tello.get_battery}%')
        
# Create and run threads for input and video
#CIC_feed = Thread(target=CIC)
#CIC_feed.start()

tello.takeoff()

movement = {'w': 0, 's': 0, 'a': 0, 'd': 0, 'space': 0, 'alt': 0, 'q': 0, 'e': 0}

while True:
    if keyboard.is_pressed('w'):
        movement['w'] = 100
        print('forward')
    if keyboard.is_pressed('s'):
        movement['s'] = 100
    if keyboard.is_pressed('a'):
        movement['a'] = 100
    if keyboard.is_pressed('d'):
        movement['d'] = 100
    if keyboard.is_pressed('space'):
        movement['space'] = 100
    if keyboard.is_pressed('c'):
        movement['c'] = 100
    if keyboard.is_pressed('q'):
        movement['q'] = 100
    if keyboard.is_pressed('e'):
        movement['e'] = 100
    tello.send_rc_control(movement['a'] - movement['d'], movement['w'] - movement['s'], movement['space'] - movement['c'], movement['q'] - movement['e'])
    movement = {'w': 0, 's': 0, 'a': 0, 'd': 0, 'space': 0, 'alt': 0, 'q': 0, 'e': 0}