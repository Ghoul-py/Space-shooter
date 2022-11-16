import pygame
import random
import math
from pygame import mixer


pygame.init()

# FPS
FPS = 90
# Score
SCORE = 0
# Screen Dimensions
WIDTH, HEIGHT = 1280,680
# Screen Color
BG_COLOR = (0, 0, 0)
# Creating Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Bullet
BULLET = pygame.transform.scale(pygame.image.load('bullet.png'),(30,30))
# Background Image
background_image = pygame.image.load('game_bg.jpg')
# Setting Caption
pygame.display.set_caption('Alien Shooter')
# loading Image from directory
icon = pygame.image.load('spaceship_red.png')
# Setting Icon 
pygame.display.set_icon(icon)

# Player
PHEIGHT = 80 # Player Height
PWIDTH = 80 # Player Width
PLAYER = pygame.image.load('spaceship.png')# Loading Player Image
PLAYER_SIZE = pygame.transform.scale(PLAYER,(PHEIGHT,PWIDTH))
VEL = 7 # Velocity of the player
PLAYERX, PLAYERY = WIDTH/2-32 , HEIGHT - 100 # Player Coordinate

# ---------------------------------------------------- #
# Enemey
ENEMY = []
ENEMYX = []
ENEMYY = []
EX = []
EY = []
num_of_enemys = 10

for i in range(num_of_enemys):
    ENEMY.append(pygame.image.load('ufo.png'))# Loading Player Image
    VEL = 7 # Velocity of the player
    ENEMYX.append(random.randint(0,WIDTH - 80))
    ENEMYY.append(random.randint(20,200)) # Player Coordinate
    EX.append(2)
    EY.append(25)
# ---------------------------------------------------- #
BULLETX = WIDTH/2
BULLETY =  HEIGHT-100# Player Coordinate
BX = 0
BY = 10
BULLET_STATE = 'ready'
# --------------------------------------- 
# SCORE_VALUE = 0
font = pygame.font.Font('freesansbold.ttf',25)
# Text Co-ordinates
TEXTY = 0
TEXTX = 0

game_over_text = pygame.font.Font('freesansbold.ttf',80)
# Text Co-ordinates
gameotextx = 640 - 230
gameotexty = 340 - 50

# Sound music
mixer.music.load('background.wav')
mixer.music.play(-1)

def Text_On_Screen(SCORE_VALUE):
    total_score = font.render('Score : '+str(SCORE_VALUE),True,(0,255,0))
    # font.render("Score : " str(SCORE_VALUE),True, (0,255,0))
    screen.blit(total_score,(TEXTX,TEXTY))

def Game_Over():
    text = game_over_text.render('Game Over',True,(255,0,0))
    screen.blit(text,(gameotextx,gameotexty))

def Player(PX):
    screen.blit(PLAYER_SIZE,(PX,PLAYERY))

def Enemy(ex,ey,i):
    screen.blit(ENEMY[i],(ex,ey))

def draw():
    """ Putting everything on the screen """
    screen.fill(BG_COLOR)
    screen.blit(background_image,(0,0))

def Fire(x,y):
    global BULLET_STATE
    BULLET_STATE = 'fire'
    screen.blit(BULLET,(x+30,y))

def isCollission(ENEMYX,ENEMYY,BULLETX,BULLETY):
    distance = math.sqrt((math.pow(ENEMYX - BULLETX,2)) + (math.pow(ENEMYY-BULLETY,2)))
    if distance < 25:
        return True
    else:
        return False


run = True
PX = WIDTH / 2 - 32
clock = pygame.time.Clock()
while run:
    draw() # calling draw function
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_LEFT] and PX > 8:
        PX -= VEL
    if key_pressed[pygame.K_RIGHT] and  PX < WIDTH - 100:
        PX += VEL

    if key_pressed[pygame.K_SPACE]:
        if BULLET_STATE == 'ready':
            firing_sound = mixer.Sound('laser.wav')
            firing_sound.play()
            BX = PX
            Fire(BX,BULLETY)
    
    if BULLETY <= 0:
        BULLETY = PLAYERY
        BULLET_STATE = 'ready'

    if BULLET_STATE == 'fire':
        Fire(BX,BULLETY)
        BULLETY -= BY

    
  
    for i in range(num_of_enemys):
        if ENEMYY[i] >= HEIGHT - 140:
            for j in range(num_of_enemys):
                ENEMYY[j] = 2000
                Game_Over()
            break

        ENEMYX[i] += EX[i]
        if ENEMYX[i] <= 0:
            EX[i] = 1.5
            ENEMYY[i] += EY[i]
        elif ENEMYX[i] >= 1180:
            EX[i] = -1.5
        collission = isCollission(ENEMYX[i],ENEMYY[i],BX,BULLETY)
        if collission:
            BULLETY = HEIGHT-100
            BULLET_STATE = 'ready'
            SCORE += 1
            ENEMYX[i] = random.randint(0,WIDTH - 80)
            ENEMYY[i] = random.randint(20,200) 
            enemy_destroyed = mixer.Sound('explosion.wav')
            enemy_destroyed.play()
        Enemy(ENEMYX[i],ENEMYY[i],i)
        Text_On_Screen(SCORE)
    Player(PX) # putting player on the screen
    
    pygame.display.update() # updatin again and again to keep everything updated
