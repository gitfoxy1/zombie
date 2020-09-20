import pygame
import random
import os
import math

import constants as c
import functions as f
from character import Hero
from character import Monster
from character import Cheater
from map import Map
from dashboard import DashboardLeft
from Items import Digle, Uzi, Kalashnikov
from backpack import Backpack
from games import Game

FPS = 60
pygame.init()
# screen = pygame.display.set_mode([100, 100])
clock = pygame.time.Clock()
game = Game(0)

run = True  # если run = False, тогда выходим из игры
while run:
    keys = pygame.key.get_pressed()
    game.keys_actions()
    for event in pygame.event.get():  # проверяем любые нажатые кнопки
        if f.exit_game(event):  # Вйти из игры если нажат знак QUIT или кнопка ESCAPE
            run = False
    # отрисовка экрана
    game.draw()
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
