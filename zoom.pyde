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
        self.bombcnt=0
        self.health=3
    
        
        
    def update(self):
        if self.keyHandler[UP]:
            self.vy = -12
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
        #print self.y
        
        if self.y <= g.h // 2:
            g.y += self.vy
        
        # print self.x
        fill(255)
        #line(self.x,self.y-g.y,self.x+self.w,self.y)

        
        #for t in g.traffic:
            #print t.y, g.y
            # if g.y < t.y:
                # print "dd"
                # g.traffic.remove(t)
                # del t
            
        if g.bombstate== False:
            for t in g.traffic:
                # print t.y, g.y    
                #fill(255)
                # line(t.x,t.y-g.y-20,t.x+t.w,t.y-g.y-20)
                if t.y-t.h < self.y < t.y+t.h  and t.x+t.w > self.x and t.x < self.x + self.w:
                    
                    #print"col",self.health, #self.y, t.y+t.h
                    g.traffic.remove(t)
                    del t
                    self.health-=1
                    if self.health==0:
                        g.state= "gameover"
                    
        
        for r in g.hearts:
            
            if r.y-r.h < self.y < r.y+r.h  and r.x+r.w > self.x and r.x < self.x + self.w:
                g.hearts.remove(r)
                del r
                self.health+=1
        
        
        t = g.policecar
        if t.y-t.h < self.y < t.y+t.h  and t.x+t.w > self.x and t.x < self.x + self.w:
                self.health=0
                if self.health==0:
                    g.state= "gameover"
                    
#display nothing for a part of time annd disable collision for bomb 
#time.time saves the value of current time
#start.time compare with the currect time and if difference become certain value enable the things again
        #print(self.bombcnt)
        for b in g.bombs:
            if b.y-b.h < self.y < b.y+b.h  and b.x+b.w > self.x and b.x < self.x + self.w:
                g.bombs.remove(b)
                del b
                self.bombcnt+=1
               
        if self.bombcnt>0 and g.bombstate== True:
            elapsed_time = time.time() - g.start_time
            print(elapsed_time)
            if elapsed_time > 4:
                g.bombstate= False
             
                        
#TODO need to figure out how to not overlap things    
                        
                    
            
                
                    
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
                self.vy = -12
            else:
                
                
                
                self.vy = -8      
            
class Traffic(Car):
    def __init__(self,x,y,img,w,h,g):
        Car.__init__(self,x,y,img,w,h,g) 
        self.x= random.randint(100,900)
        self.y= y
    #if changing random x gives u the collision with another traffici car then give another x
    def update(self):
        self.y += self.vy
        self.x += self.vx
class Bomb(Car):
    def __init__(self,x,y,img,w,h,g):
        Car.__init__(self,x,y,img,w,h,g)
        
        self.x=random.randint(200,800)
        
        self.y= random.randint(-4000,-1000)
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
        self.imgh= loadImage(path+"/images/heart.png")
        self.imgb= loadImage(path+"/images/bomb.png")
        self.policecar = policecar(512,968,"policecar.png",100,200,self.g)
        self.bombstate= False
        self.start_time=0
        self.gameStarted= False
        
        self.traffic=[]
        for i in range(20):
            self.traffic.append(Traffic(400+i*100,400-i*300,str(i%4)+".png",100,200,self.g))
            
        self.hearts = []
        for i in range(5):
            self.hearts.append(Hearts(300+i*100,300-i*400, "heart.png",50,50,self.g))
        
        self.bombs =[]
        for b in range (3):
            self.bombs.append(Bomb(500+i*100, 500-i*500, "bomb.png",50,50,self.g))
            
            
        # for t in self.traffic:
        #     print (t.x,t.y) 
    def display(self):
        y= (self.y)% self.h
        image(self.img,0,0,self.w,self.h-y,0,y,self.w,self.h)
        image(self.img,0,self.h-y,self.w,y,0,0,self.w,y)
        #image(self.imgh,15,0,50,50)
        
        self.policecar.display()
        self.zoom.display()
    
        if self.bombstate== False:
            for t in self.traffic: 
                t.display()
            
        # TODO loop through the traffics and send them above if they are below the bottom of the game
        for t in self.traffic:
            if t.y > self.zoom.y + self.h/2 :
                # if self.zoom.y < -100000: changing level
                t.y = t.y - 6000
            elif self.zoom.y < -100000:
                t.y = t.y - 1000
        for b in self.hearts:
            if b.y > self.zoom.y + self.h/2 :
                b.y = b.y -4000
        for z in self.bombs:
            if z.y > self.zoom.y + self.h/2 :
                z.y=z.y-5000
            
        
        for h in self.hearts:
            h.display()
        for b in self.bombs:
            b.display()
        
g = Game(1024,1024,668)

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
        image(g.imgh,40,0)
        textSize(40)
        text(":"+str(g.zoom.health),85,40)
    
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
        
    if keyCode == 32 and g.zoom.bombcnt > 0:
        g.bombstate= True
        g.start_time= time.time()
 
        
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
