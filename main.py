""" game zombie """
import pygame

import functions as f
from games import Game

import settings as s

FPS = 60
pygame.init()
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.music.load(s.S_BACKGROUND)
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(loops=-1)

clock = pygame.time.Clock()
game = Game(map_="MAP1", heroes=1, monsters=1, items=20)


INTRO = False  # если INTRO = False, начинается игра
RUN = True  # если RUN = False, выходим из игры
GAME_OVER = False  # если GAME_OVER = True, заставка GAME_OVER

while INTRO:
    game.characters.update()
    game.items.update()
    INTRO = game.intro()
    for event in pygame.event.get():
        if f.exit_game(event):
            INTRO = False
            RUN = False
    pygame.display.update()
    clock.tick(FPS)

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

    for event in pygame.event.get():
        if f.exit_game(event):
            RUN = False

    # GAME_OVER
    if game.all_heroes_dead():
        GAME_OVER = True

    # отрисовка экрана
    game.draw()
    if GAME_OVER:
        game.game_over()
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
