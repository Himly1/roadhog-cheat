import torch
import win32api, win32con
import pyautogui
import numpy as np
from pynput import keyboard

pyautogui.FAILSAFE = False
def takeScreenshot():
    #Will take screenshot on fullscreen
    #change the value to your window width and heigh
    frame = np.array(pyautogui.screenshot(region=(0,0,1920,1080)))
    return frame

def loadModel():
    device = torch.device('cuda:0')
    print(device)
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolo5m_1280_cheat.pt', force_reload=False)
    model.to(device)
    return model

model = None
def scan_enemy():
    frame = takeScreenshot()
    rs = model(frame)
    xyxy = rs.pandas().xyxy[0]
    return xyxy

def choose_the_enemy(enemies):
    #Fix me
    # currnetly will randomly choose an anemy
    # for ideal solution it should choose the enemy which close enough to your alignment
    enemies = enemies[enemies['confidence'] > 0.6]
    length = enemies.shape[0]

    if length > 0 :
        first_one = enemies[:1]
        return [
            first_one['xmin'].values[0].astype(int), 
            first_one['ymin'].values[0].astype(int),
            first_one['xmax'].values[0].astype(int),
            first_one['ymax'].values[0].astype(int)
            ]
    else:
        return None

lucky_guy = None
def lock_enemy():
    try:
        #Fix me
        # dont know how to convert 2d cordinates to world cordinates
        # also dont know how to find the offset of the game using cheat-engine
        # will leave this for a long time and moving on to next project
        x = 65535 // lucky_guy[0]
        y = 65535 // lucky_guy[1]
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y, 0, 0)
    except BaseException as err:
        print(f'err occred while aiming at the enemy err: ${err}')

def on_press(key):
    if(key == keyboard.Key.shift and lucky_guy != None):
        lock_enemy()

def init():
    global model 
    model = loadModel()
    lis = keyboard.Listener(on_press=on_press)
    lis.start()

init()
while True:
    enemies = scan_enemy()
    lucky_guy = choose_the_enemy(enemies=enemies)