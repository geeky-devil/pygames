import pygame
import random
import time
import math
import sys
import numpy
from math import cos,sin,sqrt

pygame.init()
screen=pygame.display.set_mode((800,600))

center_corr=(400,600)
clk=pygame.time.Clock()
x=random.randrange(0,800)
y=random.randrange(0,300)
hypo=sqrt((x-400)**2+(600-y)**2)
t=(600-y)/(400-x)
t=numpy.arctan(t)

m1=False
score=0
font =pygame.font.Font('freesansbold.ttf',24)

class bomb:
    def __init__(self):
        self.x=random.randrange(0,400)
        self.y=0
        self.rec=pygame.Rect(10,10,10,10)
        self.rec.x=self.x
        self.rec.y=y
        self.rate=random.randrange(1,8)

    def drw(self):
        pygame.draw.rect(screen,"cyan",self.rec)
        
    def get_rec(self):
        return self.rec
    def accel(self):
        self.rec.y+=self.rate
        if self.rec.y>600:
            
            self.explode(self.rec.x,self.rec.y)
            
            

    def explode(self,x,y):
        r=255
        g=0
        b=0
        for i in range(10):
            pygame.draw.circle(screen,[r,g,b],(x,y),i*2)
            g+=25
            b+=25
            time.sleep(.01)
            pygame.display.update()
            screen.fill("black")
        for i in range(10,0,-1):
            pygame.draw.circle(screen,[r,g,b],(x,y),i*2)
            g-=25
            b-=25
            time.sleep(.01)
            pygame.display.update()
            screen.fill("black")
        self.rec.x=random.randrange(0,800)
        self.rec.y=0
        self.rate=random.randrange(1,8)
i=0
counter=0
def shoot(x:list,T,s:bool):
    i=0
    new_x=(1-i*0.1)*x[0] +i*0.1*T[0]
    new_y=(1-i*0.1)*x[1] +i*0.1*T[1]
    if new_x<0 or new_x>800:
        s=False
    if new_y<0 or new_y>600:
        s=False
    pygame.draw.circle(screen,'red',(new_x,new_y),4)
    i+=.01
    pygame.display.flip()
shot=False
shot_coor=tuple()
temp_turr=tuple()
pygame.mouse.set_visible(False)
boom1= bomb()

fin=False

while True:
    screen.fill('black')
    mcorr=pygame.mouse.get_pos()
    # b_ang=math.atan2(obj_rec.y-600,obj_rec.x-400)
    t_ang=math.atan2(mcorr[1]-600,mcorr[0]-400)
    turret_x=400 +100*cos(t_ang)
    turret_y=600 +100*sin(t_ang)
    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if e.type==pygame.MOUSEBUTTONDOWN:
            m1=True
            shot=True
            shot_ang=t_ang
            nx=400+(100)*cos(shot_ang)
            ny=600+(100)*sin(shot_ang)
            temp_turr=(turret_x,turret_y)

        if e.type==pygame.MOUSEBUTTONUP:
            m1=False
    #pygame.draw.circle(screen,"cyan",(turret_x,turret_y),5,1)
    score_txt=font.render('Score:',True,'green','black')
    score_val=font.render(str(score),True,'green','black')
    txt_rec=score_txt.get_rect()
    val_rec=score_val.get_rect()
    txt_rec.center=(600,20)
    val_rec.center=(680,20)
    
    if m1:
        pygame.draw.circle(screen,"cyan",(turret_x,turret_y),10,1)
        pygame.draw.circle(screen,"cyan",(turret_x,turret_y),3)
        pygame.draw.line(screen,'green',(400,600),(turret_x,turret_y))
        # if t_ang==b_ang:
            # pygame.draw.circle(screen,'red',(400,400),10)
    if m1==False:
        pygame.draw.circle(screen,"cyan",(turret_x,turret_y),5,1)
    if shot :
        #new_x=(1-i*0.1)*shot_coor[0] +i*0.1*temp_turr[0]
        #new_y=(1-i*0.1)*shot_coor[1] +i*0.1*temp_turr[1]
        
            
        nx=400+(100-i)*cos(shot_ang)
        ny=600+(100-i)*sin(shot_ang)
        if nx<0 or nx>800:
            shot=False
            i=0
        if ny<0:
            shot=False
            i=0
        ball=pygame.draw.circle(screen,(255,0,0),(nx,ny),4)
        i-=.5
        if boom1:   
            if pygame.Rect.colliderect(ball,boom1.get_rec()):
                score+=round((ball.y/10)+boom1.rate)
                boom1.explode(ball.x,ball.y)
                ball.x=0
                ball.y=0
                shot=False
                #del boom1
               
                end=False
                i=0
                screen.blit(score_val,val_rec)
    counter+=1
    boom1.drw()
    if counter%30==0:
        boom1.accel()
        counter=0

    pygame.draw.circle(screen,"red",(400,600),3)
    
    #pygame.draw.circle(screen,"cyan",(turret_x,turret_y),3)
    #pygame.draw.aaline(screen,'green',(400,600),(turret_x,turret_y))
    pygame.draw.circle(screen,'cyan',(400,600),90,2)
    
    #screen.blit(obj_frame1,obj_rec,(0,0,30,50))
    #obj_rec.y+=1
    screen.blit(score_txt,txt_rec)
    screen.blit(score_val,val_rec)
    pygame.display.flip()

