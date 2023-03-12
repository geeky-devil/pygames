# wanted to create an explosion animation..
import numpy
import os
import time
import pygame
screen=pygame.display.set_mode((800,600))
loop=True
corr=[]

def lined():
    pygame.draw.line(screen,"red",corr)
def explosion(x,y):
    r=255
    g=0
    b=0
    for i in range(10):
        pygame.draw.circle(screen,[r,g,b],(x,y),i*2)
        g+=25
        b+=25
        time.sleep(.03)
        pygame.display.update()
        screen.fill("black")
    for i in range(10,0,-1):
       pygame.draw.circle(screen,[r,g,b],(x,y),i*2)
       g-=25
       b-=25
       time.sleep(.03)
       pygame.display.update()
       screen.fill("black")
      

while loop:   
    x=numpy.random.randint(10,780)
    y=numpy.random.randint(10,580)
    corr.append((x,y))
    explosion(x,y)
    while corr  and loop:
        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                loop=False
                break
                
        nx=numpy.random.randint(10,780)
        ny=numpy.random.randint(10,580)
        corr.append((nx,ny))
        pygame.draw.line(screen,"red",corr[0],corr[1])
        explosion(nx,ny)
        pygame.display.update()
        time.sleep(.03)
        corr.remove(corr[0])
   

