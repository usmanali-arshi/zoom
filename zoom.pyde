import time
import os, random
add_library('minim')
path = os.getcwd()
player = Minim(this)

#Level 2 starts after 31000 distance travelling and things get speed up
#initializing all cars including other objects on the road
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

    #Update of all cars               
    def update(self):
        self.x += self.vx
        self.y += self.vy
    #common display for all cars on screen
    def display(self):
        self.update()
        image(self.img,self.x,self.y-g.y,self.w,self.h,0,0,self.w,self.h)
        #rect(self.x,self.y-g.y,self.w,self.h)

#initializing the main car(zoom)
#Inheriting it from Car class
class zoom(Car):
    def __init__(self,x,y,img,w,h,g):
        Car.__init__(self,x,y,img,w,h,g)
        self.keyHandler = {LEFT:False, RIGHT:False, UP:False, DOWN:False}
        self.bombcnt=0                                                   #amount of bombs owned when the game starts
        self.health=3                                                    #at start the car's health is 3
        self.healthpolice=1                                              #if hit by a policecar the game ends automatically
        self.level=1                                                    # level when the game starts
        self.crashmusic = player.loadFile(path+"/sounds/crash.mp3")     #crashing sound when the car collides with other cars
        self.boosterValue = False
        self.comeback = False                                          #to blink the car before all the traffic comes back
        
    def display(self):
        self.update()
        if self.comeback == True and time.time() % 0.25 < 0.125:        #blinking logic
            return
        image(loadImage(path+"/images/"+g.carState),self.x,self.y-g.y,self.w,self.h,0,0,self.w,self.h)  #Isomorphism using g.carstate so that the main car (zoom) can change its display to its respective state(Booster or Zoom)      
    
    def update(self):
        if self.keyHandler[RIGHT] and self.x< g.l:
            self.vx = 12
        elif self.keyHandler[LEFT] and self.x> g.s :
            self.vx = -12
        else:
            self.vx = 0
            
        if self.keyHandler[UP]:
            self.vy = -12
            if self.keyHandler[UP] and self.boosterValue == True:             #increases speed if user has booster
                self.vy = -16  
            if self.y<-30000 and self.keyHandler[UP]:                          # increasing the speed of game after level 2
                self.vy=-18
                self.level=2 
            if self.keyHandler[UP] and self.boosterValue == True and self.y<-30000:   #increases the speed of booster even more in level 2
                self.vy=-20
                self.level=2
        else:
            self.vy=0
        
        
        #Going right and left
        if self.keyHandler[RIGHT] and self.x< g.l:
            self.vx = 12
        elif self.keyHandler[LEFT] and self.x> g.s :
            self.vx = -12
        else:
            self.vx = 0
        self.y += self.vy
        self.x += self.vx
        # so that the background starts moving when the main car reaches middle of the screen
        if self.y <= g.h // 2:
            g.y += self.vy
        #update of traffic    
        if g.bombstate== False:
            for t in g.traffic:
               #collision thoery if the Zoom(main car) hits the traffic 
                if t.y-t.h < self.y < t.y+t.h  and t.x+t.w > self.x and t.x < self.x + self.w:
                    #decreasing the health by 1 everytime it hits the traffic car
                    self.health-=1
                    self.crashmusic.play() 
                    self.crashmusic.rewind()
                    
                    #game over condition when the health of car is 0
                    if self.health==0:
                        g.state= "gameover"
                        
                    if self.healthpolice==0:
                        g.state= "gameoverbypolice"
                    
        #update of hearts
        for r in g.hearts:
            #collision of car with hearts so that it can collect it and increase its health
            if r.y-r.h < self.y < r.y+r.h  and r.x+r.w > self.x and r.x < self.x + self.w:
                #used move method cause previously deleting the cars from list made everything disappear at the end of the game
                r.move()          #randomising the position of every car after its been collided so it doesnt occur at the same place again and again
                self.health+=1      
                
                
        #update of boosters
        for p in g.boosters:
            #collision of car with boosters so that it can collect it
            if p.y-p.h < self.y < p.y+p.h  and p.x+p.w > self.x and p.x < self.x + self.w:
                p.move()
                self.boosterValue = True                    #so that its speed can be increased
                g.carState= "boost.png"                     #so that the car can change its display to booster
                
                
        
        for t in g.traffic:                                 #checking if the booster collided with 2 cars so that its state could be changed
            #collision thoery if the Zoom(main car) hits the traffic 
            if t.y-t.h < self.y < t.y+t.h  and t.x+t.w > self.x and t.x < self.x + self.w:
                t.move()
                g.boosterCheck-=1
            
            if g.boosterCheck==0:
                #checking if the booster state car has collided with 2 cars
                self.boosterValue= False                    #changing the speed of the car back to normal by changing it to False
                g.carState="zoom.png"                       #so that the car can change back to zoom
                g.boosterCheck=2                            #re initialising the counter to 2        
                
        
        #checking the collision of police car with the Zoom
        t = g.policecar
        if t.y-t.h < self.y < t.y+t.h  and t.x+t.w > self.x and t.x < self.x + self.w:
            self.healthpolice=0
            if self.healthpolice==0:
                #Instantly decreases the health of car
                g.state= "gameoverbypolice"
                    
#display nothing for a part of time annd disable collision for bomb 
#time.time saves the value of current time
#start.time compare with the currect time and if difference become certain value enable the things again
        for b in g.bombs:
            if b.y-b.h < self.y < b.y+b.h  and b.x+b.w > self.x and b.x < self.x + self.w:
                b.move()
                self.bombcnt+=1
                      #g.usedbomb to fix the bug that turned the bomb count to 0 even if the space was pressed once
        if g.bombstate== True:
            elapsed_time = time.time() - g.start_time                #calculates the elapsed time after spacebar is pressed
            
            
            if g.usedBomb == True:
                self.bombcnt=self.bombcnt-1                          #as soon as the bomb is used the count decreases
                g.usedBomb= False
            if elapsed_time > 2:                                     
                self.comeback = True
            if elapsed_time > 3:                                     #using time to use the bombfeature in the game
                g.start_time=0
                self.comeback = False
                
                g.bombstate= False

#Police Car class which chases the car                
class policecar(Car):
    def __init__(self,x,y,img,w,h,g):
        Car.__init__(self,x,y,img,w,h,g)
        self.keyHandler = {LEFT:False, RIGHT:False, UP:False, DOWN:False}
        self.police = player.loadFile(path+"/sounds/police.mp3")
        self.vy=0
    #Update is designed such that the policecar follows the zoom whereever it goes
    def update(self):
        self.y += self.vy
        self.x += self.vx
        
        if self.keyHandler[RIGHT] and self.x< g.l:
            self.vx = 12
    
        elif self.keyHandler[LEFT] and self.x> g.s :
            self.vx = -12
        else:
            self.vx = 0
        if g.gameStarted:                                #only after when UP button is pressed game is started
            if self.keyHandler[UP]:
                self.vy = -12
                self.police.play()
                if self.y<-30000:                          #police also increases speed and start chasing more fast after level 2
                    self.vy=-19
            else:
                self.vy = -8      
            
class Traffic(Car):
    def __init__(self,x,y,img,w,h,g):
        Car.__init__(self,x,y,img,w,h,g) 
        self.x= random.randint(100,900)
        self.y= y
        self.checkCollision()
    #if changing random x gives u the collision with another traffic car then give another x
     #checking collision with all other objects so no overlapping occurs      
    def checkCollision(self):
        while True:
            collisionHappened = False
            for t in g.bombs:
                if t.y-t.h < self.y < t.y+t.h  and t.x+t.w > self.x and t.x < self.x + self.w:
                    collisionHappened = True
                    break
            for h in g.hearts:
                if h.y-h.h < self.y < h.y+h.h  and h.x+h.w > self.x and h.x < self.x + self.w:
                    collisionHappened = True
                    break
            for b in g.boosters:
                if b.y-b.h < self.y < b.y+b.h  and b.x+b.w > self.x and b.x < self.x + self.w:
                    collisionHappened = True
                    break
            tmptraffic = []+g.traffic                 #to create a temp list so that it doesnt end up in an infinite loop and check that it doesnt overlap
            if self in tmptraffic:
                tmptraffic.remove(self)
            for t in tmptraffic:
                if t.y-t.h < self.y < t.y+t.h  and t.x+t.w > self.x and t.x < self.x + self.w:
                    collisionHappened = True
                    break
            if collisionHappened:
                self.x= random.randint(200,800)
                self.y= random.randint(g.zoom.y-4000,g.zoom.y-1000)
            else:
                break
    def update(self):
        self.y += self.vy
        self.x += self.vx
    def move(self):
        # updates x and y position after collision
        self.x = random.randint(200,800)
        self.y = random.randint(g.zoom.y-4000,g.zoom.y-1000)
        self.checkCollision()
        
class Bomb(Car):
    def __init__(self,x,y,img,w,h,g):
        Car.__init__(self,x,y,img,w,h,g)
        
        self.x=random.randint(200,800)
        self.y= random.randint(-4000,-1000)
        self.checkCollision()
 #checking collision with all other objects so no overlapping occurs      
    def checkCollision(self):
        while True:
            collisionHappened = False
            for t in g.traffic:
                if t.y-t.h < self.y < t.y+t.h  and t.x+t.w > self.x and t.x < self.x + self.w:
                    collisionHappened = True
                    break
            for h in g.hearts:
                if h.y-h.h < self.y < h.y+h.h  and h.x+h.w > self.x and h.x < self.x + self.w:
                    collisionHappened = True
                    break
            for b in g.boosters:
                if b.y-b.h < self.y < b.y+b.h  and b.x+b.w > self.x and b.x < self.x + self.w:
                    collisionHappened = True
                    break
            if collisionHappened:
                self.x= random.randint(200,800)
                self.y= random.randint(g.zoom.y-4000,g.zoom.y-1000)
            else:
                break
                
    def update(self):
        self.y += self.vy
        self.x += self.vx
        
    def move(self):
        # updates x and y position after collision
        self.x = random.randint(200,800)
        self.y = random.randint(g.zoom.y-4000,g.zoom.y-1000)
        self.checkCollision()
        
        
        
    

class Hearts(Car):
    def __init__(self,x,y,img,w,h,g):
        Car.__init__(self,x,y,img,w,h,g)
        self.x= random.randint(100,900)
        self.y=random.randint(-3000,-500)
        self.checkCollision()
    #checking collision with all other objects so no overlapping occurs
    def checkCollision(self):
        while True:
            collisionHappened = False
            for t in g.traffic:
                if t.y-t.h < self.y < t.y+t.h  and t.x+t.w > self.x and t.x < self.x + self.w:
                    collisionHappened = True
                    break
            for h in g.boosters:
                if h.y-h.h < self.y < h.y+h.h  and h.x+h.w > self.x and h.x < self.x + self.w:
                    collisionHappened = True
                    break
            for b in g.bombs:
                if b.y-b.h < self.y < b.y+b.h  and b.x+b.w > self.x and b.x < self.x + self.w:
                    collisionHappened = True
                    break
            if collisionHappened:
                self.x= random.randint(200,800)
                self.y= random.randint(g.zoom.y-4000,g.zoom.y-1000)
            else:
                break
    def update(self):
        self.y += self.vy
        self.x += self.vx
        
    def move(self):
        # updates x and y position after collision
        self.x = random.randint(200,800)
        self.y = random.randint(g.zoom.y-4000,g.zoom.y-1000)
        self.checkCollision()


class Boosters(Car):
    def __init__(self,x,y,img,w,h,g):
        Car.__init__(self,x,y,img,w,h,g)
        self.x= random.randint(100,900)                        #giving them random positions along the course
        self.y=random.randint(-3000,-500)
        self.checkCollision()
    #checking collision with all other objects so no overlapping occurs
    def checkCollision(self):
        while True:
            collisionHappened = False
            for t in g.traffic:
                if t.y-t.h < self.y < t.y+t.h  and t.x+t.w > self.x and t.x < self.x + self.w:
                    collisionHappened = True
                    break
            for h in g.hearts:
                if h.y-h.h < self.y < h.y+h.h  and h.x+h.w > self.x and h.x < self.x + self.w:
                    collisionHappened = True
                    break
            for b in g.bombs:
                if b.y-b.h < self.y < b.y+b.h  and b.x+b.w > self.x and b.x < self.x + self.w:
                    collisionHappened = True
                    break
            if collisionHappened:
                self.x= random.randint(200,800)
                self.y= random.randint(g.zoom.y-4000,g.zoom.y-1000)
            else:
                break
            
    def update(self):
        self.y += self.vy
        self.x += self.vx
        
    def move(self):
        # updates x and y position after collision
        self.x = random.randint(200,800)
        self.y = random.randint(g.zoom.y-4000,g.zoom.y-1000)
        self.checkCollision()


class Game:
    def __init__ (self,w,h,g):
        self.w=w
        self.h=h
        self.s=100
        self.l=self.w-100
        self.state= "menu"
        self.y =0
        self.usedBomb = False                                                      #used to tell if the bomb is used or not 
        self.boosterCheck=2                                                        #to check 2 collisions with traffic when the car is in booster state 
        self.g=g
        self.carState="zoom.png"
        self.music = player.loadFile(path+"/sounds/music.mp3")
        self.music.play()
        self.img= loadImage(path+"/images/background.png")
        self.img1= loadImage(path+"/images/menu.jpg")
        self.img2= loadImage(path+"/images/instructions.jpeg")
        self.start_distance=0                                                 #used to calculate the total score               
        self.zoom = zoom(512,600,"zoom.png",100,200,self.g)
        self.imgh= loadImage(path+"/images/heart.png")
        self.imgb= loadImage(path+"/images/bomb.png")
        self.imgbo= loadImage(path+"/images/boost.png")
        self.imgtraffic= loadImage(path+"/images/tgameover.jpg")
        self.imgpolice= loadImage(path+"/images/pgameover.jpg")
        self.policecar = policecar(512,968,"policecar.png",100,200,self.g)
        self.bombstate= False
        self.start_time=0
        self.gameStarted= False
        
        self.traffic=[]

        self.hearts = []
        
        self.boosters = []
        
        self.bombs =[]
    def createTraffic(self):
        for i in range(20):
            self.traffic.append(Traffic(400+i*100,400-i*300,str(i%4)+".png",100,200,self.g))
        
    #creating bombs and appending to the list
    def createBombs(self):
        for b in range (2):
            self.bombs.append(Bomb(500+b*100, 500-b*300, "bomb.png",50,50,self.g))
    #creating hearts
    def createHearts(self):
        for i in range(3):
            self.hearts.append(Hearts(300+i*100,300-i*300, "heart.png",50,50,self.g))
    #creating boosters
    def createBoosters(self):
        for f in range(1):
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
g.createTraffic()
g.createBombs()
g.createHearts()
g.createBoosters()

def setup():
    size(g.w, g.h)
    
def draw():
    if g.state== "menu":
        image(g.img1,0,0)
        
        
        fill(255)
        textSize(50)
    
        
        text("Press Shift to Play the Game", 20,g.h//2.5+50)
        text("Press Ctrl to Read the Instructions",20,g.h//2)
    elif g.state=="instructions":
        image(g.img2,0,0,1024,1024)
        fill(255)
        textSize(23)
        text("Hello Welcome to Zoom \nYou need to evade the traffic and outrun the police which is chasing. \nYou start with 3 lives. Everytime you hit a Car you lose a life.\nThe more distance you survive, the more you'll Score.\nThere are two Levels:\nLevel:1 Your car and police car moves at the same Speed\nLevel:2 The police car is slowly catching up to you and the game speed is also increased. \nYou can collect the following items:", 10,100)
        image(g.imgh,10,350,100,100)
        text("You can collect Hearts to Increase Your Health.",120,410)
        image(g.imgb,10,470,100,100)
        text("Use them to blast off the traffic for 3 seconds. \nPress Spacebar to use the Bomb!",120,520)
        image(g.imgbo,10,590,100,100)
        text("Use these to turn into a rocket and boost your speed. \nAfter collision with two cars, the rocket will turn back into the car!",120,630)
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
        image(g.imgtraffic,0,0,1024,1024) #displaying crashed photo
        textSize(60)
        fill (255,0,0)
        text("YOU CRASHED!",200,800)
        text("Score: "+str(end_distance),200,870)
        g.policecar.police.pause()
    
    
    elif g.state== "gameoverbypolice":
        end_distance= -(g.zoom.y)+1024 -g.start_distance
        image(g.imgpolice,0,0) #displaying BUSTED photo
        textSize(60)
        fill (255,0,0)
        text("BUSTED!",300,800)
        text("Score: "+str(end_distance),300,900)
        g.policecar.police.pause()
        
    

def keyPressed():
    if keyCode == LEFT:
        g.zoom.keyHandler[LEFT] = True
    elif keyCode == RIGHT:
        g.zoom.keyHandler[RIGHT] = True
    elif keyCode == UP:
        g.zoom.keyHandler[UP] = True
        g.gameStarted=True
#Press cntrl to view instructions
    if keyCode==17 and g.state=="menu":
        g.state="instructions"
#Press Shift to Play the Game        
    if keyCode == 16 and g.state=="menu":
        g.state= "play"  
      
#The user can press space to use the bomb which it collected        
    if keyCode == 32 and g.zoom.bombcnt > 0:
        g.bombstate= True
        g.usedBomb = True
        g.start_time= time.time()
#Press backspace to go back and return to menu
    if keyCode==8 and (g.state=="gameover" or g.state=="instructions"):
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
