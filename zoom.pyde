import time
import os, random
path = os.getcwd()

class Car:
    def __init__ (self,x,y,r,img,w,h,g):
        self.x=x
        self.y=y
        self.r=r
    
        self.w=w
        self.h=h
        self.vx=0
        self.vy=0
        self.g=g
        self.img = loadImage(path+"/images/"+img)

        
    def update(self):
        if self.y+self.r >= self.g:
            self.vy=0
        else:
            self.vy += 0.3
            if self.y + self.r + self.vy > self.g:
                self.vy = self.g - (self.y+self.r)
        
        self.x += self.vx
        self.y += self.vy
                
    def display(self):
        self.update()
        
        image(self.img,self.x-self.w//2,self.y-self.h//2+30,self.w - 200,self.h - 400,0,0,self.w,self.h)
    
class zoom(Car):
    def __init__(self,x,y,r,img,w,h,g):
        Car.__init__(self,x,y,r,img,w,h,g)
        self.keyHandler = {LEFT:False, RIGHT:False, UP:False, DOWN:False}
        
    def update(self):

        if self.keyHandler[UP]:
            self.vy = -5
        elif self.keyHandler[DOWN]:
            self.vy = 5
        else:
            self.vy = 0

        if self.keyHandler[RIGHT]:
            self.vx = 12
        elif self.keyHandler[LEFT]:
            self.vx = -12
        else:
            self.vx = 0
        
        self.y += self.vy
        self.x += self.vx


class Game:
    def __init__ (self,w,h,g):
        self.w=w
        self.h=h
        self.g=g
        self.img= loadImage(path+"/images/background.png")
        self.zoom = zoom(512,768,-50,"zoom.png",300,620,self.g)
        
    def display(self):
        
        image(self.img,0,0)
    
        self.zoom.display()
  
        
g = Game(1024,768,668)

def setup():
    size(g.w, g.h)
    
def draw():
    background(0)
    g.display()

def keyPressed():
    if keyCode == LEFT:
        g.zoom.keyHandler[LEFT] = True
    elif keyCode == RIGHT:
        g.zoom.keyHandler[RIGHT] = True
    elif keyCode == UP:
        g.zoom.keyHandler[UP] = True

        
def keyReleased():
    if keyCode == LEFT:
        g.zoom.keyHandler[LEFT] = False
    elif keyCode == RIGHT:
        g.zoom.keyHandler[RIGHT] = False
    elif keyCode == UP:
        g.zoom.keyHandler[UP] = False
