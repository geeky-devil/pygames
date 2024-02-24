import pygame,os,time,sys,random,threading
pygame.init()
SCREEN_WIDTH=800
SCREEN_HEIGHT=600
screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

run=True
clock=pygame.time.Clock()

#Variables
selected_trail = 0  # default
jump_count=0
distance=0
pos=[380,180]
delay=200
upper_bound=random.randint(0,delay)
timer=0
obstacles=[]
spike_speed=5
ground_color=[0,255,0]
color_list=["white","red","pink","green","orange","purple","blue","cyan","yellow"]
color_list2=["cyan","white","pink"]
RED=(255,0,0)
WHITE=(255,255,255)

rec=pygame.Rect(800,590,200,10)
spike=pygame.image.load("spike.png")
spike=pygame.transform.scale(spike,(32,32))

spike_rect=spike.get_rect()
spike_rect.center=(1000,581)
spike_group=pygame.sprite.Group()
ground=pygame.rect.Rect(0,598,800,5)
player_x=200
player_y=400
player_rect=pygame.rect.Rect(player_x,player_y,3,30)
ground_y=598
num_evaded=0
def reset_game():
    global spike_speed,spike_group,timer,upper_bound,distance,jump_count,player_x,player_y,num_evaded,player_rect
    jump_count=0
    distance=0
    spike_speed=5
    timer=0
    upper_bound=random.randint(0,delay)
    player_rect.x=player_x
    player_rect.y=player_y
    num_evaded=0
    spike_group.empty()

def player_movement(spikes,spike_group):
    collisions=player_rect.collidedictall(spikes)
    if collisions:
        player_rect.x-=15
        for spike,_ in collisions:
            spike_group.remove(spike)
        #remove the sprite 
        if player_rect.x<0:
            game_over_menu()
            #reset player to original pos
    
def draw_trail(player_x,player_y):
    global ground_y
    for i in range(0,abs(ground_y-player_y),10):
        trail_rect=pygame.rect.Rect(player_x+random.randrange(-10,10),player_y+i+30,5,2)
        pygame.draw.rect(screen,"pink",trail_rect,5) 
def draw_trail2(player_x,player_y):
    global ground_y
    last_x=player_x
    for i in range(0,abs(ground_y-player_y),10):
        last_x=last_x+random.randrange(-10,10)
        trail_rect=pygame.rect.Rect(last_x,player_y+i+30,5,10)
        pygame.draw.rect(screen,"white",trail_rect,5)  

def draw_trail3(player_x,player_y):
    global ground_y,color_list
    for i in range(0,abs(ground_y-player_y),10):
        width=5*(i//10)
        trail_rect=pygame.rect.Rect(player_x-width//2,player_y+i+30,5*(i//10),5)
        pygame.draw.rect(screen,color_list[random.randint(0,8)],trail_rect,5)  
        
def draw_trail4(player_x,player_y):
    global ground_y,color_list
    gradient_color = [
        int(RED[i] + (WHITE[i] - RED[i]) * (player_y / SCREEN_HEIGHT))
        for i in range(3)
    ]
    for i in range(0,abs(ground_y-player_y),10):
        width=5*(i//10)
        trail_rect=pygame.rect.Rect(player_x-width//6,player_y+i+30,5*(i//30),5)
        #pygame.draw.rect(screen,color_list[random.randint(0,8)],trail_rect,5)  
        pygame.draw.rect(screen,gradient_color,trail_rect,5)  

def draw_trail5(player_x,player_y):
    global ground_y
    for i in range(0,abs(ground_y-player_y),30):
        width=5*(i//10)
        trail_rect=pygame.rect.Rect(player_x-width//6,player_y+i+30,5*(i//30),5*(i//60))
        pygame.draw.rect(screen,"cyan",trail_rect,1)  

def draw_trail6(player_x,player_y):
    global ground_y,color_list2
    
    for i in range(0,abs(ground_y-player_y),30):
        width=5*(i//10)
        trail_rect=pygame.rect.Rect(random.randrange(-30,30)+player_x-width//6,player_y+i+30,5*(i//30),5*(i//60))
        pygame.draw.rect(screen,color_list2[random.randint(0,2)],trail_rect,1)  
def draw_spike():
    global spike_group,num_evaded,run
    for spikes in spike_group.sprites():     
        screen.blit(spike,spikes.rect)
        spikes.rect.center=[spikes.rect.center[0]-spike_speed,spikes.rect.center[1]]
        if spikes.rect.center[0]<-42:
            spike_group.remove(spikes)
            num_evaded+=1
            
        pygame.display.flip()
    
       

def draw_stats(text, font, color, surface, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


#TRAIL PRESETS
    #1 looks like a whirlwind
    #2 trail3 looks like  rocket thrust
    # trail4 is sharper version of 3
    # trail 5 same as 4 but wit rectangles

#BOOLEANS
jump=False


def event_handler():
    global jump,jump_count,run,spike_group

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
            pygame.quit()
            sys.exit
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE and player_rect.y==570: 
                jump=True
                jump_count+=1
            if event.key == pygame.K_ESCAPE:
                pause_menu()
    
                
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_SPACE:
                jump=False
        
        

def main_loop():
    global run,distance,ground,ground_y,spike_group,spike_rect,spike_speed,delay,upper_bound,timer,jump,jump_count
    while run:
        event_handler()
        screen.fill("black")
        clock.tick(120)
        timer+=1
        draw_stats("Distance "+str(distance),font2,"green",screen,550,10)
        draw_stats("Jumps "+str(jump_count),font2,"green",screen,700,10)
        pygame.draw.rect(screen,"cyan",player_rect,1,3)
        pygame.display.flip()
        pygame.draw.rect(screen,ground_color,ground,10) # GROUND DRAWN HERE <--
        distance+=spike_speed
        print("DIST:",distance,end="\r")
        if num_evaded//spike_speed>3:
            spike_speed+=1
         
            
        
        if jump:
            if player_rect.y<300:
                player_rect.y=300
                jump=False
            player_rect.y-=10
            #TRAIL HERE <------------
            if selected_trail == 1:
                draw_trail(player_rect.x,player_rect.y)
            elif selected_trail == 2:
                draw_trail2(player_rect.x,player_rect.y)
            elif selected_trail == 3:
                draw_trail3(player_rect.x,player_rect.y)
            elif selected_trail == 4:
                draw_trail4(player_rect.x,player_rect.y)
            elif selected_trail == 5:
                draw_trail5(player_rect.x,player_rect.y)
            elif selected_trail == 6:
                draw_trail6(player_rect.x,player_rect.y)
            

        if jump==False and player_rect.y<568:
            player_rect.y+=10



        player_movement(spike_group.spritedict,spike_group)
        if timer>=upper_bound:
            timer=0
            upper_bound=random.randint(0,delay)
            
        
            spk=pygame.sprite.Sprite()
            spk.image=spike
            spk.rect=spike_rect.copy()
            if len(spike_group.sprites())>0:
                spike_group.add(spk)            
            else:
                
                spk=pygame.sprite.Sprite()
                spk.image=spike
                spk.rect=spike_rect.copy()
                spike_group.add(spk)
        draw_spike()
        draw_stats("Distance "+str(distance),font2,"green",screen,550,10)
        draw_stats("Jumps "+str(jump_count),font2,"green",screen,700,10)
        pygame.display.update()


############## Start MENU ##################
font = pygame.font.Font(None, 36)
font2 = pygame.font.Font(None, 24)
font3=pygame.font.Font(None,42)
pygame.display.set_caption("Endless")
def draw_text(text, font, color, surface, x, y):
    global color_list
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)
def start_menu():
    while True:
        time.sleep(.05)
        screen.fill("white")
        draw_text("Start Menu", font, "black", screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4 - 100)
        draw_text("Press SPACE to Start", font, "black", screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100)
        draw_text("Press O for Settings", font, color_list[random.randint(0,8)], screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT / 2)
        draw_text("Press ESC to Quit", font, "red", screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4)
        
        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Start the game
                    main_loop()
                    return
                elif event.key==pygame.K_o:
                    settings_menu()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

################ Pause menu#################
def pause_menu():
    paused = True
    while paused:
        screen.fill("white")
        draw_text("Paused", font, "black", screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
        draw_text("Press P to Continue", font, "black", screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        draw_text("Press Q to Quit", font, "red", screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4)
        draw_text("Press S for Start Menu", font, "blue", screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3/4 +100 )
        
        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
                elif event.key==pygame.K_s:
                    paused=False
                    reset_game()
                    start_menu()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
######### GAMEOVER MENU####################
def game_over_menu():
    global distance,jump_count
    game_over = True
    distance+=(distance/10)*jump_count
    distance=int(distance/10)
    color_list=["white","red","pink","green","orange","purple","blue","cyan","yellow"]
    while game_over:
        screen.fill("cyan")
        draw_text("Score "+str(distance),font3,color_list[random.randint(0,8)],screen,SCREEN_WIDTH / 2, SCREEN_HEIGHT / 8)
        draw_text("Game Over", font, "black", screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
        draw_text("Press R to Retry", font, "black", screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        draw_text("Press S for Start Menu", font, "black", screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4)
        
        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Restart the game
                    reset_game()
                    game_over = False
                elif event.key == pygame.K_s:
                    # Go to start menu
                    reset_game()
                    start_menu()

###### TRAIL MENU##################
pygame.display.set_caption("Jump Trail Settings")
def settings_menu():
    global selected_trail,clock
    menu_running = True
    text_surface = pygame.Surface((SCREEN_WIDTH//2, SCREEN_HEIGHT))
    color_list=["white","red","pink","green","orange","purple","blue","cyan","yellow"]
    text_surface.fill("black")
    while menu_running:
        screen.fill("cyan")
        draw_text("Jump Trail 0", font,"white", text_surface, 200, 50)
        draw_text("Jump Trail 1", font, "white", text_surface, 200, 100)
        draw_text("Jump Trail 2", font, "white", text_surface, 200, 150)
        draw_text("Jump Trail 3", font, "white", text_surface, 200, 200)
        draw_text("Jump Trail 4", font, "white", text_surface, 200, 250)
        draw_text("Jump Trail 5", font, "white", text_surface, 200, 300)
        draw_text("Jump Trail 6", font, "white", text_surface, 200, 350)
        draw_text("PRESS RETURN TO SELECT AND GO BACK", font2, "white", text_surface, 200, 400)
        screen.blit(text_surface,(0,10))
        
        prev_rec=player_rect.copy() #copy used to preview trail animation
        prev_rec.x=600
        prev_rec.y=598
        for i in range(40):
            clock.tick(120)
            screen.fill("black")
            screen.blit(text_surface,(0,10))
            prev_rec.y-=10
            if selected_trail == 0:
                draw_text("Jump Trail 0", font,color_list[random.randint(0,8)], text_surface, 200, 50)
            elif selected_trail == 1:
                draw_text("Jump Trail 1", font, color_list[random.randint(0,8)], text_surface, 200, 100)
                draw_trail(prev_rec.x,prev_rec.y)
            elif selected_trail == 2:
                draw_text("Jump Trail 2", font, color_list[random.randint(0,8)], text_surface, 200, 150)
                draw_trail2(prev_rec.x,prev_rec.y)
            elif selected_trail == 3:
                draw_text("Jump Trail 3", font, color_list[random.randint(0,8)], text_surface, 200, 200)
                draw_trail3(prev_rec.x,prev_rec.y)
            elif selected_trail == 4:
                draw_text("Jump Trail 4", font, color_list[random.randint(0,8)], text_surface, 200, 250)
                draw_trail4(prev_rec.x,prev_rec.y)
            elif selected_trail == 5:
                draw_text("Jump Trail 5", font, color_list[random.randint(0,8)], text_surface, 200, 300)
                draw_trail5(prev_rec.x,prev_rec.y)
            elif selected_trail == 6:
                draw_text("Jump Trail 6", font, color_list[random.randint(0,8)], text_surface, 200, 350)
                draw_trail6(prev_rec.x,prev_rec.y)
            pygame.draw.rect(screen,"blue",prev_rec,1,3)
            screen.blit(text_surface,(0,10))
            
            pygame.display.flip()
        prev_rec.y=598   
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    selected_trail = 0
                elif event.key == pygame.K_1:
                    selected_trail = 1
                elif event.key == pygame.K_2:
                    selected_trail = 2
                elif event.key == pygame.K_3:
                    selected_trail = 3
                elif event.key == pygame.K_4:
                    selected_trail = 4
                elif event.key == pygame.K_5:
                    selected_trail = 5
                elif event.key == pygame.K_6:
                    selected_trail = 6
                elif event.key == pygame.K_RETURN:
                    menu_running = False

start_menu()



