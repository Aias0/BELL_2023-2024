import keyboard, time
camera_up = True
while True:
    time.sleep(0.3)
    if keyboard.is_pressed('tab') and not camera_up:
        print('up')
        camera_up = True
    elif keyboard.is_pressed('tab'):
        print('down')
        camera_up = False