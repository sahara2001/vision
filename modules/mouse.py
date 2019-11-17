import pyautogui as gui
import math

class Mouse:

    def __init__(self, width, height, depth):
        """ initialize a mouse controller, use three argument to adjust sensitivity in each dimention"""
        self.width = width
        self.height = height
        self.depth = depth
        self.pos=[0,0]
    
    def disp(self):
        pyautogui.moveTo(self.pos[0], self.pos[1],duration = 1) 

    def mov(self, angler,anglec, dr,dc):
        dr += self.depth * math.atan(angler) 
        dc += self.depth * math.atan(anglec)
        self.pos[0] += dr
        self.pos[1] += dc

    def reset(self):
        self.pos=[0,0]
        self.disp()

    def set_w(self,w):
        self.width = w
        self.reset()
    
    def set_h(self,h):
        self.height = h
        self.reset()

    def set_d(self,d):
        self.depth = d
        self.reset()
