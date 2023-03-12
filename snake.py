from math import ceil
import numpy
from pickle import TRUE
import pygame
from pygame.locals import *
import os
pygame.init()
screen=pygame.display.set_mode((800,600))
pygame.display.set_caption("advance snake")    
class OBJ:
    def __init__(self:pygame.Rect) -> None:
        self.x=300
        self.y=300
        self.color=[0,255,200]
        self.size=(10,10)
        self.pos=[]
        self.pcount=-1
        self.head=pygame.Rect((self.x,self.y),(self.size))
    def draw(self):
        self.pos.append((self.x,self.y))
        self.pcount+=1
        return pygame.draw.rect(screen,self.color,((self.x,self.y),(self.size)))
    def drawt(self,tail):
        return pygame.draw.rect(screen,self.color,(self.pos[len(self.pos)-5*tail],(self.size)))
    def incx(self)->int:
        if self.x>=780:
            self.x=780
        self.x+=5
    def decx(self)->int:
        if self.x<=10:
            self.x=10
        self.x-=5
    def decy(self)->int:
        if self.y<=10:
            self.y=10
        self.y-=5
    def incy(self)->int:
        if self.y>=580:
            self.y=580
        self.y+=5
    def update(sefl):
        pygame.display.update()
    def posclear(self,tail:int):
        self.pos.pop()
        
class tar():
    def __init__(self) -> None:
        self.color=[250,0,0]
        self.radius=5
        self.x=round(numpy.random.randint(0,780),-1)
        self.y=round(numpy.random.randint(0,580),-1)
    def draw(self):
        return pygame.draw.circle(screen,self.color,(self.x,self.y),5)    
        
    def reloc(self):
        self.x=round(numpy.random.randint(10,780),-1)
        self.y=round(numpy.random.randint(10,580),-1)
        
s=OBJ()
t=tar()
run=1
tail=0
lk=False
rk=False
uk=False
dk=False
while run!=0:
    clk=pygame.time.Clock()
    clk.tick(59)
    screen.fill([0,0,0])
    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            run=0
        key=pygame.key.get_pressed()
        if e.type==pygame.KEYDOWN:
            if e.key==pygame.K_LEFT:
                lk=True
            if e.key==pygame.K_RIGHT:
                rk=True
            if e.key==pygame.K_UP:
                uk=True
            if e.key==pygame.K_DOWN:
                dk=True

        elif e.type==pygame.KEYUP:
            if e.key==pygame.K_LEFT:
                lk=False
            if e.key==pygame.K_RIGHT:
                rk=False
            if e.key==pygame.K_UP:
                uk=False
            if e.key==pygame.K_DOWN:
                dk=False
          
    if lk:
        s.decx()
    elif rk:
        s.incx()
    elif uk:
        s.decy()
    elif dk:
        s.incy()
    
    if s.x+5 in range(t.x-5,t.x+5) or s.x in range(t.x-5,t.x+5):
        if s.y+5 in range(t.y-5,t.y+5) or s.y in range(t.y-5,t.y+5):
            t.reloc()
            tail+=1
            s.posclear(tail)
            
    if tail>0:
        for i in range(tail,0,-1):
            s.drawt(i)
        for i in range(len(s.pos),len(s.pos)-5*tail):
            s.pos.pop()      
    s.draw()
    t.draw()
    s.update()
    

        
