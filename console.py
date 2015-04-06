
import pygame, math, sys
from pygame.locals import *

class Button:
    def __init__(self, text, x  = 0, y = 0, w = 100, h = 500, color = (170,170,170)):
        self.loc = (x,y)
        self.dim = (w,h)
        self.color = color
        self.onclick = lambda:None

    def displayOn(self,console):
        console.makeRectangle(self.loc[0],self.loc[1],self.dim[0],self.dim[1],self.color)

class Pane:
    def __init__(self,x = 0, y = 0, w = 100, h = 500, resolution = 3, color = (170,170,170)):
        self.loc = (x,y)
        self.dim = (w,h)
        self.color = color
        self.res = resolution
        self.rects = []
        
    def plot(self, loc1,loc2,color = (0,0,0)):
        self.rects.append((loc1,loc2,color))

    def displayOn(self, console):
        console.makeRectangle(self.loc[0],self.loc[1],self.dim[0],self.dim[1],self.color)
        for i in self.rects:
            console.makeRectangle(self.loc[0]+i[0][0],self.loc[1]+i[0][1],i[1][0]-i[0][0],i[1][1]-i[0][1],i[2])
        

class Console:
    maxFPS = 20 # 10
    def __init__(self, W = 650, H = 650):
        self.w, self.h, self.surface = W, H, pygame.display.set_mode( ( W, H ) )
        pygame.display.set_caption('Tristan\'s Downfall')
        self.bgc = (80, 80, 80)
        self.extraIOHandler = lambda x: None
        
    def update(self):
        pygame.display.update()

    def flood(self, color = None):
        self.surface.fill(self.bgc)
        
    def makeLine(self, start_pos, end_pos, color = (0, 0, 0)):
        pygame.draw.line(self.surface, color, start_pos, end_pos)
        
    def makeRectangle(self, x, y, width, height, color = (0, 0, 0) ):
        pygame.draw.rect( self.surface, list( color ), pygame.Rect( x , y , width, height ) )

    def handleIO(self):
        for e in pygame.event.get():
            if e.type == QUIT:
                self.close()
            self.extraIOHandler(e)

    def close(self):
        pygame.quit()
        sys.exit()

con = Console()
b_listen = Button('listen',10,40,150,80)
b_calibrate = Button('calibrate',10,300,300,80)
p_calibrate = Pane(350,300,250,100)

for i in range(10):
    p_calibrate.plot((19+22*i,45),(34+22*i,60))

while True:
    con.handleIO()
    con.flood()
    b_listen.displayOn(con)
    b_calibrate.displayOn(con)
    p_calibrate.displayOn(con)
    con.update()
    
