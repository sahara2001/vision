import pyautogui as gui
import math

class Mouse:

    def __init__(self, width, height, depth):
        """ initialize a mouse controller, use three argument to adjust sensitivity in each dimention"""
        self.width = width
        self.height = height
        self.depth = depth
        self.pos=[1,1]
    
    def disp(self):
        gui.moveTo(self.pos[0], self.pos[1],duration = gui.MINIMUM_DURATION) 

    def mov(self, angler,anglec, dr,dc):
        dr += self.depth * math.atan(angler) 
        dc += self.depth * math.atan(anglec)
        self.pos[0] += dr
        self.pos[1] += dc
        self.disp()

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



if __name__ == "__main__":
    controller = Mouse(1280,720,500)

    for i in range(1,1000,50):
        controller.mov(0,0,50,50)
