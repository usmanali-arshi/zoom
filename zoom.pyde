import time
import os, random

add_library('minim')
path = os.getcwd()
player = Minim(this)

#Level 2 starts after 16000 distance travelling and things get speed up
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
        self.music = 0
                
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
        self.health=3 #at start the car's health is 3
        self.level=1
        # self.boosterCheck=2
        #self.bs_distance=0
        # self.bl_distance=0
        self.boosterValue = False
        # if self.boosterValue==True:
            
        #     self.img = loadImage(path+"/images/boost.png")
        # else:
        #     self.img = loadImage(path+"/images/zoom.png")
    
        
        
    def update(self):
        if self.keyHandler[UP] and self.boosterValue == True:
            self.vy = -16
            self.music = player.loadFile(path+"/sounds/police.mp3")
            self.music.play()
        elif self.keyHandler[UP]:
            self.vy = -12
            self.music = player.loadFile(path+"/sounds/police.mp3")
            self.music.play()
        elif self.y<-15000: #level:2 starts and speeds up the game
                self.vy=-18
                self.level=2
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
        #update of traffic    
        if g.bombstate== False:
            for t in g.traffic:
               #collision thoery if the Zoom(main car) hits the traffic
                
                if t.y-t.h < self.y < t.y+t.h  and t.x+t.w > self.x and t.x < self.x + self.w:
                    g.traffic.remove(t)
                    del t
                    g.boosterCheck-=1
                    #decreasing the health by 1 everytime it hits the traffic car
                    self.health-=1 
                    
                    #game over condition when the health of car is 0
                    if self.health==0:
                        g.state= "gameover"
                    
        #update of hearts
        for r in g.hearts:
            #collision of car with hearts so that it can collect it
            if r.y-r.h < self.y < r.y+r.h  and r.x+r.w > self.x and r.x < self.x + self.w:
                g.hearts.remove(r)
                del r
                self.health+=1
                
                
        #update of boosters
        for p in g.boosters:
            #collision of car with boosters so that it can collect it
            if p.y-p.h < self.y < p.y+p.h  and p.x+p.w > self.x and p.x < self.x + self.w:
                g.boosters.remove(p)
                del p
                self.boosterValue = True
            
                print g.boosterCheck
                self.img = loadImage(path+"/images/boost.png")
                if g.boosterCheck==0:
                    print("hey")
                    #self.boosterValue= False
                
                
                # self.bs_distance= self.y
                # self.bl_distance= self.bs_distance-1000
                # print self.y, self.bl_distance
                # if self.y<self.bl_distance:
                #     print("hey")
                #     self.boosterValue=False
                
                
                
                

        
        #checking the collision of police car with the Zoom
        t = g.policecar
        if t.y-t.h < self.y < t.y+t.h  and t.x+t.w > self.x and t.x < self.x + self.w:
                self.health=0
                if self.health==0:
                    #Instantly decreases the health of car
                    g.state= "gameover"
                    
#display nothing for a part of time annd disable collision for bomb 
#time.time saves the value of current time
#start.time compare with the currect time and if difference become certain value enable the things again
        for b in g.bombs:
            if b.y-b.h < self.y < b.y+b.h  and b.x+b.w > self.x and b.x < self.x + self.w:
                g.bombs.remove(b)
                del b
                self.bombcnt+=1
#used bomb to fix the bug that turned the bomb count to 0 even if the space was pressed once


        if self.bombcnt>0 and g.bombstate== True:
            elapsed_time = time.time() - g.start_time
            if g.usedBomb == True:
                self.bombcnt=self.bombcnt-1
                g.usedBomb= False
            print(elapsed_time)
            if elapsed_time > 3:
                g.start_time=0
                
                g.bombstate= False
#TODO after you use bombs three times the elapsed time doesnt change (fix)
                        
#TODO need to figure out how to not overlap things    

#TODO blink the car after 2.5 sec of using bomb

#Police Car class which chases the car                
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
                if self.y<-15000:#police also increases speed and start chasing more fast after level 2
                    self.vy=-16.2
            else:
                self.vy = -8      
            
class Traffic(Car):
    def __init__(self,x,y,img,w,h,g):
        Car.__init__(self,x,y,img,w,h,g) 
        self.x= random.randint(100,900)
        self.y= y
    #if changing random x gives u the collision with another traffic car then give another x
    def update(self):
        self.y += self.vy
        self.x += self.vx
class Bomb(Car):
    def __init__(self,x,y,img,w,h,g):
        Car.__init__(self,x,y,img,w,h,g)
        
        self.x=random.randint(200,800)
        self.y= random.randint(-4000,-1000)
        self.checkCollision()
 #checking collision with traffic so it doesnt overlaps the car       
    def checkCollision(self):

         for t in g.traffic:
              if t.y-t.h < self.y < t.y+t.h  and t.x+t.w > self.x and t.x < self.x + self.w:
                self.x= random.randint(100,900)
                self.y= random.randint(-4000,-1000)
    def update(self):
        self.y += self.vy
        self.x += self.vx
        
    

class Hearts(Car):
    def __init__(self,x,y,img,w,h,g):
        Car.__init__(self,x,y,img,w,h,g)
        self.x= random.randint(100,900)
        self.y=random.randint(-3000,-500)
        self.checkCollision()
    #checking that the hearts dont have the same position as traffic and bombs
    def checkCollision(self):
        for t in g.traffic:
             if t.y-t.h < self.y < t.y+t.h  and t.x+t.w > self.x and t.x < self.x + self.w:
                 self.x= random.randint(100,900)
                 self.y= random.randint(-3000,-500)
        for b in g.bombs:
             if b.y-b.h < self.y < b.y+b.h  and b.x+b.w > self.x and b.x < self.x + self.w:
                 self.x= random.randint(100,900)
                 self.y= random.randint(-3000,-500)
    def update(self):
        self.y += self.vy
        self.x += self.vx


class Boosters(Car):
    def __init__(self,x,y,img,w,h,g):
        Car.__init__(self,x,y,img,w,h,g)
        self.x= random.randint(100,900)
        self.y=random.randint(-3000,-500)
        self.checkCollision()
    
    def checkCollision(self):
        for v in g.boosters:
             if v.y-v.h < self.y < v.y+v.h  and v.x+v.w > self.x and v.x < self.x + self.w:
                 self.x= random.randint(100,900)
                 self.y= random.randint(-3000,-500)
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
        self.usedBomb = False
        self.boosterCheck=2
        self.music = player.loadFile(path+"/sounds/music.mp3")
        self.music.play()
        self.g=g
        self.img= loadImage(path+"/images/background.png")
        self.img1= loadImage(path+"/images/menu.jpg")
        self.img2= loadImage(path+"/images/instructions.jpeg")
        self.start_distance=0
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
        
        self.boosters = []
        
        self.bombs =[]
        
    #creating bombs and appending to the list
    def createBombs(self):
        for b in range (3):
            self.bombs.append(Bomb(500+b*100, 500-b*300, "bomb.png",50,50,self.g))
    #creating hearts
    def createHearts(self):
        for i in range(5):
            self.hearts.append(Hearts(300+i*100,300-i*300, "heart.png",50,50,self.g))
    #creating boosters
    def createBoosters(self):
        for f in range(3):
            self.boosters.append(Boosters(300+f*100,300-f*300, "boost.png",150,100,self.g))

        
#looping the background image to keep them in the frame        
    def display(self):
        y= (self.y)% self.h
        image(self.img,0,0,self.w,self.h-y,0,y,self.w,self.h)
        image(self.img,0,self.h-y,self.w,y,0,0,self.w,y)
        #image(self.imgh,15,0,50,50)
        
        self.policecar.display()
        self.zoom.display()
    # So that when user use bombs it gives an illusion that it has blasted everything on the screen so it doesnt show the screen and there is no collision with the traffic either
        if self.bombstate== False:
            for t in self.traffic: 
                t.display()
            
        #loops through the traffics and send them above if they are below the bottom of the game
        for t in self.traffic:
            if t.y > self.zoom.y + self.h/2 :
                # if self.zoom.y < -100000: changing level
                t.y = t.y - 6000
            elif self.zoom.y < -100000:
                t.y = t.y - 1000
         #loops through the hearts and send them above if they are below the bottom of the game
        for b in self.hearts:
            if b.y > self.zoom.y + self.h/2 :
                b.y = b.y -random.randint(2000,4000)
         #loops through the bombs and send them above if they are below the bottom of the game
        for z in self.bombs:
            if z.y > self.zoom.y + self.h/2 :
                z.y = z.y-4000
        
        #loops through the bombs and send them above if they are below the bottom of the game
        for v in self.boosters:
            if v.y > self.zoom.y + self.h/2 :
                v.y = v.y-4000
                
        
        for h in self.hearts:
            h.display()
        for t in self.boosters:
            t.display()
        for b in self.bombs:
            b.display()
        
g = Game(1024,1024,668)
g.createBombs()
g.createHearts()
g.createBoosters()

def setup():
    size(g.w, g.h)
    
def draw():
    if g.state== "menu":
        image(g.img1,0,0)
        
        
        fill(255,0,0)
        textSize(50)
        fill(255)
        
        text("Press Shift to Play the Game", g.w//3,g.h//2.5)
        text("Press Ctrl to Read the Instructions",g.w//5,g.h//2)
    elif g.state=="instructions":
        image(g.img2,0,0,1024,1024)
        fill(255)
        textSize(23)
        text("Hello Welcome to Zoom \nYou need to evade the traffic and outrun the police which is chasing. \nYou start with 3 lives. Everytime you hit a Car you lose a life.\nThe more distance you survive, the more you'll Score.\nThere are two Levels:\n Level:1 Your car and police car moves at the same Speed\nLevel:2 The police car is slowly catching up to you and the game speed is also increased. \nYou can collect the following items:", 10,100)
        image(g.imgh,10,350,100,100)
        text("You can collect Hearts to Increase Your Health.",120,410)
        image(g.imgb,10,470,100,100)
        text("Use them to blast off the traffic for 3 seconds. \nPress Spacebar to use the Bomb!",120,520)
        textSize(20)
        text("Press BackSpace to return to the menu",500,950)
    elif g.state=="play":
        background(0)    
        
        g.display()
        image(g.imgh,40,0) #displaying hearts photo
        image(g.imgb,40,50) #displaying bomb photo
        
        textSize(40)
        text(":"+str(g.zoom.health),85,40)
        text(":"+str(g.zoom.bombcnt),85,90)
        textSize(30)
        text("Level: "+str(g.zoom.level),880,40)
        
        
    
    elif g.state== "gameover":
        end_distance= -(g.zoom.y)+1024 -g.start_distance
        textSize(50)
        fill (255,0,0)
        text("GAME OVER",g.w//2.5, g.h//3)
        text("Score: "+str(end_distance),g.w//3+80,g.h//3+100) 

def keyPressed():
    if keyCode == LEFT:
        g.zoom.keyHandler[LEFT] = True
    elif keyCode == RIGHT:
        g.zoom.keyHandler[RIGHT] = True
    elif keyCode == UP:
        g.zoom.keyHandler[UP] = True
        g.gameStarted=True
    if keyCode==17:
        g.state="instructions"
#Press Shift to Play the Game        
    if keyCode == 16:
        g.state= "play"    
#The user can press space to use the bomb which it collected        
    if keyCode == 32 and g.zoom.bombcnt > 0:
        g.bombstate= True
        g.usedBomb = True
        g.start_time= time.time()
    if keyCode==8:
        g.state="menu"
 
        
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
