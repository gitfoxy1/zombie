""" game zombie """
# pylint: disable=no-member

import pygame

import functions as f
from games import Game

FPS = 60
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
# screen = pygame.display.set_mode([100, 100])
clock = pygame.time.Clock()
game = Game(map_="MAP1", heroes=1, monsters=0, items=20)

RUN = True  # если run = False, тогда выходим из игры
GAME_OVER = False
while RUN:
    # update
    game.characters.update()
    game.items.update()
    if game.is_characters_in_cell():
        # обновляет счётчики, если у героя закончился действия, то ход переходит к следующему герою
        counters = game.update_counters()
        # добавляет монстров каждую волну
        if counters.wave:
            game._init_monsters_wave()

        active_character = game.get_active_character()
        if active_character.type == "hero":
            game.hero_actions()
        elif active_character.type == "monster":
            game.monster_actions()

    for event in pygame.event.get():  # проверяет любые нажатые кнопки
        if f.exit_game(event):  # Вйти из игры если нажат знак QUIT или кнопка ESCAPE
            RUN = False

    # GAME_OVER
    if game.all_heroes_dead():
        GAME_OVER = True

    # отрисовка экрана
    game.draw()
    if GAME_OVER:
        game.draw_game_over()
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
