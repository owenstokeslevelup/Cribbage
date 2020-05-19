import pygame
import random

#set up the bubble brain
class Bubble():
    # Bubble class Cunstructor Function
    def __init__(self, x, y):
        # make somme variables for the bubble
        self.x = x
        self.y = y
        self.speed = random.randint (1, 3)
        self.pic = pygame.image.load ("../assets/Bubble.png")
        self.on_screen = True


        #shrink the pic
        self.pic = pygame.transform.scale(self.pic, (15, 15))

# bubble update function
    def update (self, screen):
        self.y -= self.speed
        screen.blit(self.pic, (self.x, self.y))

        if self.y < -self.pic.get_height():
            self.on_screen = False
        
          
#end of Bubble class

# Set up the Enemy's brain
class Enemy():
    #enemy constructor function
    def __init__(self, x, y, speed, size):
        #make enemy variables
        self.x = x      
        self.y = y
        # randome enemies
        self.type = random.randint(0,3)
        if self.type == 0:
            self.pic = pygame.image.load("../assets/Fish06_A.png")
            self.pic2 = pygame.image.load("../assets/Fish06_B.png")
        if self.type == 1:
            self.pic = pygame.image.load("../assets/Fish05_A.png")
            self.pic2 = pygame.image.load("../assets/Fish05_B.png")
        if self.type == 2:
            self.pic = pygame.image.load("../assets/Fish02_A.png")
            self.pic2 = pygame.image.load("../assets/Fish02_B.png")
        if self.type == 3:
            self.pic = pygame.image.load("../assets/Fish03_A.png")
            self.pic2 = pygame.image.load("../assets/Fish03_B.png")
            
        self.speed = speed
        self.size = size
        self.hitbox = pygame.Rect(self.x, self.y, int(self.size*1.25), self.size)
        self.anamation_timer_max = 16
        self.anamation_timer = self.anamation_timer_max
        self.anamation_frame = 0
        # shrink the enemy pic
        self.pic = pygame.transform.scale(self.pic, (int (self.size*1.25), self.size))
        self.pic2 = pygame.transform.scale(self.pic2, (int (self.size*1.25), self.size))
        
        # flip enemy pic
        if self.speed < 0:
            self.pic = pygame.transform.flip(self.pic, True, False)
            self.pic2 = pygame.transform.flip(self.pic2, True, False)
            

    #enemy update function
    def update(self, screen):
        self.anamation_timer -= 1
        if self.anamation_timer <= 0:
            self.anamation_timer = self.anamation_timer_max
            self.anamation_frame += 1
            if self.anamation_frame > 1:
                self.anamation_frame = 0
        self.x += self.speed
        self.hitbox.x += self.speed
       # pygame.draw.rect(screen, (255, 0, 255), self.hitbox)
        if self.anamation_frame == 0:
            screen.blit(self.pic, (self.x, self.y))
        else:
            screen.blit(self.pic2, (self.x, self.y))
            

#end of enemy class

# Start the game
pygame.init()
game_width = 1000
game_height = 650
screen = pygame.display.set_mode((game_width, game_height))
clock = pygame.time.Clock()
running = True
#picture's hear for game
background_pic = pygame.image.load("../assets/Scene_A.png")
background_pic2 = pygame.image.load("../assets/Scene_B.png")
player = random.randint(0,4)
if player== 0:
    player_pic = pygame.image.load("../assets/Fish04_A.png")
    player_pic3 = pygame.image.load("../assets/Fish04_B.png")
    player_pic2 = pygame.image.load("../assets/Fish04_open.png")
if player == 1:
    player_pic = pygame.image.load("../assets/Fish05_A.png")
    player_pic3 = pygame.image.load("../assets/Fish05_B.png")
    player_pic2 = pygame.image.load("../assets/Fish05_open.png")
if player == 2:
    player_pic = pygame.image.load("../assets/Fish06_A.png")
    player_pic3 = pygame.image.load("../assets/Fish06_B.png")
    player_pic2 = pygame.image.load("../assets/Fish06_open.png")
if player == 3:
    player_pic = pygame.image.load("../assets/Fish03_A.png")
    player_pic3 = pygame.image.load("../assets/Fish03_B.png")
    player_pic2 = pygame.image.load("../assets/Fish03_open.png")
if player == 4:
    player_pic = pygame.image.load("../assets/Fish02_A.png")
    player_pic3 = pygame.image.load("../assets/Fish02_B.png")
    player_pic2 = pygame.image.load("../assets/Fish02_open.png")



# make timers for background anamation
bg_anamation_timer_max = 25
bg_anamation_timer = bg_anamation_timer_max
bg_anamation_frame = 0





#Make some variables for player
player_starting_x = 480
player_starting_y = 310
player_starting_size = 30
player_x = player_starting_x
player_y = player_starting_y
player_speed = 0.3
player_speed_x = 0
player_speed_y = 0
player_stop = 0
player_size = player_starting_size
player_facing_left = False
player_hitbox = pygame.Rect(player_x, player_y, int(player_size*1.25), player_size)
player_alive = False


#make player open/close timer
player_eating_timer_max = 6
player_eating_timer = 0
player_swimming_timer_max = 8
player_swimming_timer = player_swimming_timer_max
player_swimming_frame = 0

#make variables for HUD (heads-up desplay)
score = -1
score_font = pygame.font.SysFont("default", 30)
score_text = score_font.render("Score:"+str(score),1, (250,250,250))

play_button_pic = pygame.image.load("../assets/BtnPlayIcon.png")
play_button_x = game_width/2 - play_button_pic.get_width()/2
play_button_y = game_height/2 - play_button_pic.get_height()/2
title_pic = pygame.image.load("../assets/title.png")
title_x = game_width/2 - title_pic.get_width()/2
title_y = play_button_y - 250

#enemy timers
enemy_timer_max = 25
enemy_timer = enemy_timer_max

# make the enemys array
enemies = []
enemies_to_remove = []

#make bubbles array
bubbles = []
bubbles_to_remove = []
bubble_timer = 0




# ***************** Loop Land Below *****************
# Everything under 'while running' will be repeated over and over again
while running:
    # Makes the game stop if the player clicks the X or presses esc
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
    # Check to see what keys the player is preesing
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        player_speed_x += player_speed
    if keys[pygame.K_LEFT]:
        player_speed_x -= player_speed
    if keys[pygame.K_UP]:
        player_speed_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_speed_y += player_speed

    #if keys[pygame.K_SPACE]:
        #player_speed_x = player_stop
    #if keys[pygame.K_SPACE]:
        #player_speed_y = player_stop
    


    # make player slow down
    if player_speed_x > 1:
        player_speed_x -= 0.1
    if player_speed_x < -1:
        player_speed_x += 0.1
    if player_speed_y > 1:
        player_speed_y -= 0.1
    if player_speed_y < -1:
        player_speed_y += 0.1


        
    if keys[pygame.K_SPACE]:
        player_size += 2
    #if keys[pygame.K_z]:
    #  player_size -= 2

    # move  the player
    player_x += player_speed_x
    player_y += player_speed_y


    # player flip
    if player_speed_x > 0:
        player_facing_left = False
    else:
        player_facing_left = True
        
    #stop player leaving screen
    if player_x < 0:
        player_x = 0
        player_speed_x = 0
    if player_x > game_width - player_size*1.25:
        player_x = game_width - player_size*1.25
        player_speed_x = 0
    if player_y < 0:
        player_y = 0
        player_speed_y = 0
    if player_y > game_height - player_size:
        player_y = game_height - player_size
        player_speed_y = 0
    

    
    

   #make pictures show up in game
    bg_anamation_timer -= 1
    if bg_anamation_timer <= 0:
        bg_anamation_frame += 1
        if bg_anamation_frame >1:
            bg_anamation_frame = 0
        bg_anamation_timer = bg_anamation_timer_max


    if bg_anamation_frame == 0:
        screen.blit(background_pic, (0, 0))
    else:
        screen.blit(background_pic2, (0, 0))
        
#enemy timer user hits 0 spawn
    enemy_timer-= 1
    if enemy_timer <= 0:
        new_enemy_y = random.randint(0, game_height)
        new_enemy_speed = random.randint(2, 5)
        new_enemy_size = random.randint(player_size/2, player_size*2)\
                         
        if random.randint(0, 1) == 0:
            enemies.append(Enemy(-new_enemy_size*2 , new_enemy_y, new_enemy_speed, new_enemy_size))
        else:
            enemies.append(Enemy(game_width, new_enemy_y, -new_enemy_speed, new_enemy_size))
        enemy_timer = enemy_timer_max


    for enemy in enemies_to_remove:
        enemies.remove(enemy)
    enemies_to_remove = []

    
    #update all the enemys
    for enemy in enemies:
        enemy.update(screen)
        if enemy.x < -1000 or enemy.x > game_width+1000:
            enemies_to_remove.append(enemy)
    # make new bubble when timer = 0
    bubble_timer -= 1
    if bubble_timer <= 0:
        bubbles.append(Bubble(400,490))
        bubbles.append(Bubble(460,460))
        bubble_timer = random.randint(40, 90)

    # update all bubbles
    for bubble in bubbles:
        if bubble.on_screen:
            bubble.update(screen)
        else:
            bubbles_to_remove.append(bubble)

        # remove the bubbles in bubbles to remove
    for bubble in bubbles_to_remove:
        bubbles.remove(bubble)
    bubbles_to_remove = []
            

    
    
            
        
    if player_alive:
       
        #update player hitbox
        player_hitbox.x = player_x
        player_hitbox.y = player_y
        player_hitbox.width = int(player_size * 1.25)
        player_hitbox.height = player_size
        #pygame.draw.rect(screen, (255, 255, 255), player_hitbox)
    
        
        #check to see when the player hits enemy
        for enemy in enemies:
            if player_hitbox.colliderect(enemy.hitbox):
                if player_size >= enemy.size:
                    score += enemy.size
                    player_size += 2
                    enemies.remove(enemy)
                    player_eating_timer = player_eating_timer_max
                else:
                    player_alive = False
      
        # do the player swimming animation timer
        player_swimming_timer -= 1
        if player_swimming_timer <= 0:
            player_swimming_timmer = player_swimming_timer_max
            player_swimming_frame += 1
            if player_swimming_frame > 1:
                player_swimming_frame = 0

        # draw player pic
        if player_eating_timer > 0:
            player_pic_small = pygame.transform.scale(player_pic2, (int(player_size *1.25), player_size))
            player_eating_timer-= 1
        else:
            if player_swimming_frame ==0:  
               player_pic_small = pygame.transform.scale(player_pic, (int(player_size *1.25), player_size))
            else:
                player_pic_small = pygame.transform.scale(player_pic3, (int(player_size *1.25), player_size))
        if player_facing_left:
            player_pic_small = pygame.transform.flip(player_pic_small, True, False)
        screen.blit(player_pic_small,(player_x, player_y))



        #score text draw
        if player_alive:
            score_text = score_font.render("Score: "+str(score), 1, (250,250,250))
        else:
            score_text = score_font.render("Final Score: "+str(score), 1, (250, 250, 250))
    if score >= 0:
       screen.blit(score_text,(30, 30))
           

    # draw menu (when player is not alive)
    if not player_alive:
        screen.blit(play_button_pic, (play_button_x, play_button_y))
        screen.blit(title_pic, (title_x, title_y))
        mouse_x, mouse_y = pygame.mouse.get_pos()
    #check to see if player cliks the play button
        if pygame.mouse.get_pressed()[0]:
            if mouse_x > play_button_x and mouse_x < play_button_x+play_button_pic.get_width():
                if mouse_y > play_button_y and mouse_y <play_button_y+play_button_pic.get_height():
                    #restart the game
                    player_alive = True
                    score = 0
                    player_x = player_starting_x
                    player_y = player_starting_y
                    player_size = player_starting_size
                    player_speed_x = 0
                    player_speed_y = 0
                    for enemy in enemies:
                        enemies_to_remove.append(enemy)
                    
                    
                    


    # Tell pygame to update the screen
    #blit pics
    pygame.display.flip()
    clock.tick(50)
    pygame.display.set_caption("MY GAME fps: " + str(clock.get_fps()))
