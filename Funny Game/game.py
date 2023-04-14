import random
from os import listdir
import pygame
from pygame. constants import QUIT, K_DOWN, K_UP, K_RIGHT, K_LEFT

pygame.init()
FPS = pygame.time.Clock()
screen = width, height = 1200, 700

# My colors (RGB)
BLACK = 0,0,0
WHITE = 255,255,255
GRAY = 155,155,155
YELLOW = 255,255,0
BLUE = 0, 0, 255
RED = 255, 0, 0
GREEN = 0, 255, 0



# Scores
scores = 0
font = pygame.font.SysFont("Verdana", 20)



# Our player
IMAGES_PATH = 'goose'
main_surface = pygame.display.set_mode(screen)
player_images = [pygame.transform.scale(pygame.image.load(IMAGES_PATH + '/' + file).convert_alpha(),(135,90)) for file in listdir(IMAGES_PATH)]
player = player_images[0]
player_rect = player.get_rect()
player_speed = 5
# ----------------------------------------
CHANGE_GOOSE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_GOOSE, 125)
img_index = 0

# Bonus
def create_bonus():
    bonus = pygame.transform.scale(pygame.image.load("images/bonus.png").convert_alpha(),(60,100))
    bonus_rect = pygame.Rect(random.randint(0,width), 0, *bonus.get_size())
    bonus_speed = random.randint(2,5)
    return [bonus, bonus_rect, bonus_speed]
# ----------------------------------------
CREATE_BONUS = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_BONUS, 1500)
bonuses = []

# Enemy
def create_enemy():
    enemy = pygame.transform.scale(pygame.image.load("images/enemy.png").convert_alpha(),(80,40))
    enemy_rect = pygame.Rect(width, random.randint(0,height), *enemy.get_size())
    enemy_speed = random.randint(2, 5)
    return [enemy, enemy_rect, enemy_speed]
# -----------------------------------------
CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)
enemies = []

# Background
bg = pygame.transform.scale(pygame.image.load("images/background.png").convert(),screen)
bgX = 0
bgX2 = bg.get_width()
bg_speed = 3


# Game
is_working = True
while is_working:
    FPS.tick(100)
    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False

        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())

        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())

        if event.type == CHANGE_GOOSE:
            img_index += 1
            if img_index == len(player_images):
                img_index = 0
            player = player_images[img_index]

    # remove blurring of other objects on the background
    bgX -= bg_speed
    bgX2 -= bg_speed
    if bgX < -bg.get_width():
        bgX = bg.get_width()
    if bgX2 < -bg.get_width():
        bgX2 = bg.get_width()
    main_surface.blit(bg, (bgX, 0))
    main_surface.blit(bg, (bgX2, 0))

    # make the counter and the player visible on the screen
    main_surface.blit(player, player_rect)
    main_surface.blit(font.render(str(scores), True, RED), (width - 30, 0))

    # make the enemy visible
    # make it move to the left side of the screen in a different places relative to height
    # the object will be deleted after leaving the screen
    # game will stop if we catch it
    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2], 0)
        main_surface.blit(enemy[0], enemy[1])
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

        if player_rect.colliderect(enemy[1]):
            is_working = False

    # make the bonuses visible
    # make it move to the bottom of the screen in a different places relative to width
    # the object will be deleted after leaving the screen or if we catch it
    # counter on the right top side of the screen will show us how many bonuses we catch
    for bonus in bonuses:
        bonus[1] = bonus[1].move(0, bonus[2])
        main_surface.blit(bonus[0], bonus[1])
        if bonus[1].bottom > height:
            bonuses.pop(bonuses.index(bonus))

        if player_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            scores += 1

    # put into action our keys on the keyboard (up, down, right, left)
    # limit the fields for our player
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_DOWN] and not player_rect.bottom >= height:
        player_rect = player_rect.move(0, player_speed)

    if pressed_keys[K_UP] and not player_rect.top <= 0:
        player_rect = player_rect.move(0, -player_speed)

    if pressed_keys[K_RIGHT] and not player_rect.right >= width:
        player_rect = player_rect.move(player_speed, 0)

    if pressed_keys[K_LEFT] and not player_rect.left <= 0:
        player_rect = player_rect.move(-player_speed, 0)

    # Output
    pygame.display.flip()

