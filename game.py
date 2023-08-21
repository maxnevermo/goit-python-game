import random
import os
import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT
pygame.init()

def createEnemy():
    enemySize = (30,30)
    enemy = pygame.image.load('enemy.png').convert_alpha()
    enemyPos = pygame.Rect(WIDTH, random.randint(250, HEIGHT-250), *enemySize)
    enemyMove = [random.randint(-8,-4),0]
    return [enemy, enemyPos, enemyMove]

def createBonus():
    bonusSize = (10,10)
    bonus = pygame.image.load('bonus.png').convert_alpha()
    bonusPos = pygame.Rect(random.randint(400, WIDTH-400), 0, *bonusSize)
    bonusMove = [0, random.randint(4,8)]
    return [bonus, bonusPos, bonusMove]



HEIGHT = 800
WIDTH = 1200
WHITE_COLOR = (255,255,255)
BLACK_COLOR = (0,0,0)
BLUE_COLOR = (0,0,255)
PLAYER_SIZE = (20,20)
FONT = pygame.font.SysFont('Verdana', 20)
IMAGE_PATH = "Goose"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)
imageIndex = 0

CREATE_ENEMY = pygame.USEREVENT + 1
CREATE_BONUS = pygame.USEREVENT + 2
CHANGE_IMAGE = pygame.USEREVENT + 3

pygame.time.set_timer(CREATE_ENEMY, 1500)
pygame.time.set_timer(CREATE_BONUS, 2700)
pygame.time.set_timer(CHANGE_IMAGE, 200)

bg = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH, HEIGHT))
bgX1 = 0
bgX2 = bg.get_width()
bgMoveSpeed = 3

FPS = pygame.time.Clock()

mainWindow = pygame.display.set_mode((WIDTH, HEIGHT))

player = pygame.image.load('player.png').convert_alpha()

initial_player_x = 200
initial_player_y = 250
PLAYER_POS = pygame.Rect(initial_player_x, initial_player_y, PLAYER_SIZE[0], PLAYER_SIZE[1])


playerMoveDown = [0,4]
playerMoveUp = [0,-4]
playerMoveRight = [4,0]
playerMoveLeft = [-4,0]

playing = True
enemies = []
bonuses = []
score = 0

while playing:
    FPS.tick(260)
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(createEnemy())
        if event.type == CREATE_BONUS:
            bonuses.append(createBonus())
        if event.type == CHANGE_IMAGE:
            player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[imageIndex]))
            imageIndex += 1
            if imageIndex == len(PLAYER_IMAGES):
                imageIndex = 0
    
    bgX1 -= bgMoveSpeed
    bgX2 -= bgMoveSpeed

    if bgX1 < -bg.get_width():
        bgX1 = bg.get_width()

    if bgX2 < -bg.get_width():
        bgX2 = bg.get_width()

    mainWindow.blit(bg, (bgX1,0))
    mainWindow.blit(bg, (bgX2,0))

    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and PLAYER_POS.bottom <= HEIGHT:
        PLAYER_POS = PLAYER_POS.move(playerMoveDown)

    if keys[K_UP] and PLAYER_POS.top > 0:
        PLAYER_POS = PLAYER_POS.move(playerMoveUp)

    if keys[K_RIGHT] and PLAYER_POS.right <= WIDTH:
        PLAYER_POS = PLAYER_POS.move(playerMoveRight)

    if keys[K_LEFT] and PLAYER_POS.left > 0:
        PLAYER_POS = PLAYER_POS.move(playerMoveLeft)

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        mainWindow.blit(enemy[0], enemy[1])

        if PLAYER_POS.colliderect(enemy[1]):
            playing = False

    for bonus in bonuses:
         bonus[1] = bonus[1].move(bonus[2])
         mainWindow.blit(bonus[0], bonus[1])

         if PLAYER_POS.colliderect(bonus[1]):
            score += 1
            bonuses.pop(bonuses.index(bonus))


    mainWindow.blit(player,PLAYER_POS)
    mainWindow.blit(FONT.render(str(score), True, BLACK_COLOR), (WIDTH-50, 20))
    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))
            
    for bonus in bonuses:
        if bonus[1].bottom >= HEIGHT:
            bonuses.pop(bonuses.index(bonus))