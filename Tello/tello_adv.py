import time, cv2, keyboard, logging
from djitellopy import Tello
from threading import Thread
import numpy as np
from bell_tello import Bell_Tello
sys.path.insert(1, 'Common_Data/')
HAZARD_LIST = None
from data import *
from support import *

start_time = time.time()
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
        if keyboard.is_pressed('q'):
            tello.streamoff()
            tello.close_graph()
            exit()
        if keyboard.is_pressed('tab'):
            tello.toggle_video_direction()
        # Info
        if tello.get_battery() < 5:
            logging.critical(f'Battery dangerously low. {tello.get_battery()}%')
        elif tello.get_battery() < 10:
            logging.warning(f'Battery low. {tello.get_battery()}%')
        first_run = False
        
# Create and run threads for input and video
CIC_feed = Thread(target=CIC)
#CIC_feed.daemon(True)
CIC_feed.start()

# Movement commands
tello.takeoff()
time.sleep(1)
tello.current_pos[2] = tello.get_height()
def test(*kwargs):
    pass
tello.move_pos(
    (116, 39, 30), #Move to school building
)

tello.set_video_direction(Tello.CAMERA_DOWNWARD)
time.sleep(0.5)
tello.payload_release() # Drop firejumper
time.sleep(0.5)
tello.set_video_direction(Tello.CAMERA_FORWARD)

tello.land_ground_pad()
auto_time_left = 30 - (start_time - time.time())
if auto_time_left > 0:
    time.sleep(auto_time_left) # Wait out rest of 30 sec auto period

# Going to scan red/blue screen
tello.move_pos(
    (404, 120, 120), # Move to top of highest building on right
)
time.sleep(2)
tello.move_pos(
    (424, 85, 90), # Move to scanning position
)
tello.rotate_clockwise(180)

# Seeing tower screen is Red or Blue
tower_scan = tello.get_frame_read().frame
tower_scan = cv2.cvtColor(tower_scan, cv2.COLOR_RGB2BGR)
# Processing Scan
mask1 = cv2.inRange(tower_scan, (0,50,20), (5,255,255))
mask2 = cv2.inRange(tower_scan, (175,50,20), (180,255,255))
mask = cv2.bitwise_or(mask1, mask2)
scan_red = False
if cv2.countNonZero(mask) > 0:
    scan_red = True
# Showing Scan
tower_color = cv2.resize(tower_scan, (360, 240))
rb = {'Red': True, 'Blue': False}
tower_color = cv2.putText(tower_color, f'Color: {rb[scan_red]}')
cv2.imshow('Tower Scan', tower_scan)
cv2.moveWindow('Tower Scan', 40,30)
time.sleep(1)
tello.rotate_counter_clockwise(180)

# Land at Firebuilding Pad
tello.land_building_pad()

# Closing and cleaning up
running = False
CIC_feed.join()
tello.streamoff()
tello.close_graph()