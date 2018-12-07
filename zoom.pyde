import time
import os, random
path = os.getcwd()

class Car:
    def __init__ (self,x,y,r,img,w,h,g):
        self.x=x
        self.y=y
        self.r=r
        self.s=100
        self.l=1000
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
        
        image(self.img,self.x-self.w//6,self.y-self.h//6-g.y,self.w/3,self.h/3,0,0,self.w,self.h)
    
class zoom(Car):
    def __init__(self,x,y,r,img,w,h,g):
        Car.__init__(self,x,y,r,img,w,h,g)
        self.keyHandler = {LEFT:False, RIGHT:False, UP:False, DOWN:False}
        
    def update(self):

        if self.keyHandler[UP]:
            self.vy = -5
        else:
            self.vy = 0

        if self.keyHandler[RIGHT] and self.x+self.r< self.l:
            self.vx = 12
        elif self.keyHandler[LEFT] and self.x+self.r> self.s :
            self.vx = -12
        else:
            self.vx = 0
        
        self.y += self.vy
        self.x += self.vx
        
        print self.y
        
        if self.y <= g.h // 2:
            g.y += self.vy



class Game:
    def __init__ (self,w,h,g):
        self.w=w
        self.h=h
        self.y =0
        self.g=g
        self.img= loadImage(path+"/images/background.png")
        self.zoom = zoom(512,768,-50,"zoom.png",300,620,self.g)
        
    def display(self):
        y= (self.y)% self.h
        image(self.img,0,0,self.w,self.h-y,0,y,self.w,self.h)
        image(self.img,0,self.h-y,self.w,y,0,0,self.w,y)
        
    
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
