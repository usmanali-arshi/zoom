import time
import os, random
path = os.getcwd()


class Car:
    def __init__ (self,x,y,img,w,h,g):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.vx=0
        self.vy=0
        self.g=g
        self.img = loadImage(path+"/images/"+img)

        
    def update(self):
        if self.y>= self.g:
            self.vy=0
        else:
            self.vy += 0.3

        
        self.x += self.vx
        self.y += self.vy
                
    def display(self):
        self.update()
        
        image(self.img,self.x,self.y-g.y,self.w,self.h,0,0,self.w,self.h)
        #rect(self.x,self.y-g.y,self.w,self.h)
    
class zoom(Car):
    def __init__(self,x,y,img,w,h,g):
        Car.__init__(self,x,y,img,w,h,g)
        self.keyHandler = {LEFT:False, RIGHT:False, UP:False, DOWN:False}
        self.health=3
        self.booster = False
    
        
        
    def update(self):
        if self.keyHandler[UP] and self.booster == True:
            self.vy = -12
        elif self.keyHandler[UP]:
            self.vy = -6
        else:
            self.vy = 0


        if self.keyHandler[RIGHT] and self.x< g.l:
            self.vx = 12
        elif self.keyHandler[LEFT] and self.x> g.s :
            self.vx = -12
        else:
            self.vx = 0
            
        
        
        self.y += self.vy
        self.x += self.vx

        
        if self.y <= g.h // 2:
            g.y += self.vy

        fill(255)
            
        
        for t in g.traffic:
            if t.y-t.h < self.y < t.y+t.h  and t.x+t.w > self.x and t.x < self.x + self.w:
                
                print"col",self.health, #self.y, t.y+t.h
                g.traffic.remove(t)
                del t
                self.health-=1
                if self.health==0:
                    g.state= "gameover"
                    
        
        for r in g.hearts:
            print(r.y)
            if r.y-r.h < self.y < r.y+r.h  and r.x+r.w > self.x and r.x < self.x + self.w:
                g.hearts.remove(r)
                del r
                self.health+=1
        
        for v in g.boosts:
            print(v.y)
            if v.y-v.h < self.y < v.y+v.h  and v.x+v.w > self.x and v.x < self.x + self.w:
                self.vy = 0
                g.boosts.remove(v)
                del v
                self.booster = True
                self.img = loadImage(path+"/images/boost.png")
        
        
        t = g.policecar
        if t.y-t.h < self.y < t.y+t.h  and t.x+t.w > self.x and t.x < self.x + self.w:
                self.health=0
                if self.health==0:
                    g.state= "gameover"
        

                    
class policecar(Car):
    def __init__(self,x,y,img,w,h,g):
        Car.__init__(self,x,y,img,w,h,g)
        self.keyHandler = {LEFT:False, RIGHT:False, UP:False, DOWN:False}
        #self.vy = random.randint(-8,-6)
        
    def update(self):
        self.y += self.vy
        self.x += self.vx
        
        if self.keyHandler[RIGHT] and self.x< g.l:
            self.vx = 12
    
        elif self.keyHandler[LEFT] and self.x> g.s :
            self.vx = -12
        else:
            self.vx = 0
        if g.gameStarted:
            if self.keyHandler[UP]:
                self.vy = -6
            else:
                self.vy = -4      
            
class Traffic(Car):
    def __init__(self,x,y,img,w,h,g):
        Car.__init__(self,x,y,img,w,h,g) 
        self.x= random.randint(100,900)
        self.y= y
    def update(self):
        self.y += self.vy
        self.x += self.vx
        
class Hearts(Car):
    def __init__(self,x,y,img,w,h,g):
        Car.__init__(self,x,y,img,w,h,g)
        #check if the traffic and hearts are colliding if they are randomise again
        self.x= random.randint(100,900)
        self.y=random.randint(-3000,-500)
    def update(self):
        self.y += self.vy
        self.x += self.vx

class Boosts(Car):
    def __init__(self,x,y,img,w,h,g):
        Car.__init__(self,x,y,img,w,h,g)
        #check if the traffic and boosts are colliding if they are randomise again
        self.x= random.randint(100,900)
        self.y=random.randint(-3000,-500)
    def update(self):
        self.y += self.vy
        self.x += self.vx



class Game:
    def __init__ (self,w,h,g):
        self.w=w
        self.h=h
        self.s=100
        self.l=self.w-100
        self.state= "menu"
        self.y =0
        self.g=g
        self.img= loadImage(path+"/images/background.png")
        self.img1= loadImage(path+"/images/menu.jpg")
        self.zoom = zoom(512,600,"zoom.png",100,200,self.g)
        self.policecar = policecar(512,968,"policecar.png",100,200,self.g)
        self.gameStarted= False
        self.time = 0
        self.timeCnt = 0
        
        self.traffic=[]
        for i in range(100):
            self.traffic.append(Traffic(400+i*100,400-i*300,str(i%4)+".png",100,200,self.g))
            
        self.hearts = []
        for i in range(5):
            self.hearts.append(Hearts(300+i*100,300-i*400, "heart.png",50,50,self.g))
        
        self.boosts = []
        for i in range(10):
            self.boosts.append(Boosts(300+i*100,300-i*400, "boost.png",100,178,self.g))
            
    
    def display(self):
        y= (self.y)% self.h
        image(self.img,0,0,self.w,self.h-y,0,y,self.w,self.h)
        image(self.img,0,self.h-y,self.w,y,0,0,self.w,y)
    
    
        self.policecar.display()
        self.zoom.display()
    
        
        
        for t in self.traffic:
            t.display()
            
        for h in self.hearts:
            h.display() 
        
        for z in self.boosts:
            z.display() 
    
    
        
g = Game(1024,768,668)

def setup():
    size(g.w, g.h)
    
def draw():
    if g.state== "menu":
        image(g.img1,0,0)
        
        
        fill(255,0,0)
        textSize(40)
        fill(255)
        
        text("Press Shift to Play the Game", g.w//2.5,g.h//3)
    elif g.state=="play":
        background(0)    
        g.display()
    
    elif g.state== "gameover":
        textSize(50)
        fill (255,0,0)
        text("GAME OVER",g.w//2.5, g.h//3)

def keyPressed():
    if keyCode == LEFT:
        g.zoom.keyHandler[LEFT] = True
    elif keyCode == RIGHT:
        g.zoom.keyHandler[RIGHT] = True
    elif keyCode == UP:
        g.zoom.keyHandler[UP] = True
        g.gameStarted=True
        
    if keyCode == 16:
        g.state= "play"    
        
    if keyCode == RIGHT:
        g.policecar.keyHandler[RIGHT] = True
    elif keyCode == LEFT:
        g.policecar.keyHandler[LEFT] = True
    
    if keyCode == UP:
        g.policecar.keyHandler[UP] = True
        
def keyReleased():
    if keyCode == LEFT:
        g.zoom.keyHandler[LEFT] = False
    elif keyCode == RIGHT:
        g.zoom.keyHandler[RIGHT] = False
    elif keyCode == UP:
        g.zoom.keyHandler[UP] = False
        
        
    if keyCode == RIGHT:
        g.policecar.keyHandler[RIGHT] = False
    elif keyCode == LEFT:
        g.policecar.keyHandler[LEFT] = False
        
    if keyCode == UP:
        g.policecar.keyHandler[UP] = False
