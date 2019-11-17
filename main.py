import numpy as np
import pyautogui as gui


gui.moveTo(1, 1,duration = 0.01) 

# gui.moveTo(100, 100,duration = 0.01) 



for i in range(60):
    gui.moveTo(100+i, 100+i,duration = 0.01) 