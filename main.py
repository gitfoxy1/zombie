""" game zombie """
# pylint: disable=no-member

import pygame

import functions as f
from games import Game


FPS = 60
pygame.init()
# screen = pygame.display.set_mode([100, 100])
clock = pygame.time.Clock()
game = Game(heroes=1, monsters=1, map_id=1)

RUN = True  # если run = False, тогда выходим из игры
while RUN:

    # обновляет счётчики, если у героя закончился действия, то ход переходит к следующему герою
    counters = game.update_counters()
    # добавляет монстров каждую волну
    if counters.wave:
        game.init_monsters_wave()

    active_character = game.get_active_character()
    if active_character.type == "hero":
        game.hero_actions()
    elif active_character.type == "monster":
        game.monster_actions()

    for event in pygame.event.get():  # проверяет любые нажатые кнопки
        if f.exit_game(event):  # Вйти из игры если нажат знак QUIT или кнопка ESCAPE
            RUN = False
    # отрисовка экрана
    game.draw()
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
