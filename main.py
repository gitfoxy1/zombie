""" game zombie """
# pylint: disable=no-member

import pygame

import functions as f
from games import Game


FPS = 60
pygame.init()
# screen = pygame.display.set_mode([100, 100])
clock = pygame.time.Clock()
game = Game(1)

RUN = True  # если run = False, тогда выходим из игры
while RUN:
    keys = pygame.key.get_pressed()
    game.keys_actions()
    for event in pygame.event.get():  # проверяем любые нажатые кнопки
        if f.exit_game(event):  # Вйти из игры если нажат знак QUIT или кнопка ESCAPE
            RUN = False
    # отрисовка экрана
    game.draw()
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
