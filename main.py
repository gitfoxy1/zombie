""" game zombie """
import time

import pygame
from pygame.rect import Rect

import functions as f
import settings as s
from game import Game
from game_menu import *
from text import Text
from menu import Menu
from pygame import Surface

# todo
#  udar kulakom, mimo nuzhen zvuk promaha

FPS = 60
pygame.init()
pygame.display.set_caption("zombies")
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.music.load(s.S_BACKGROUND)
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(loops=-1)

clock = pygame.time.Clock()
screen = f.init_screen()
MENU = True
menu = Menu(screen)
f.intro_1(screen=screen, delay=10)
HEROES = f.menu_heroes(screen=screen)
MAP = "map"
MONSTERS = 0
ITEMS = 20
game = Game(screen=screen, map_=MAP, heroes=HEROES, monsters=MONSTERS, items=ITEMS + ((HEROES - 1) * 10))

INTRO = True  # если INTRO = False, начинается игра
RUN = True  # если RUN = False, выходим из игры
GAME_OVER = False  # если GAME_OVER = True, заставка GAME_OVER
counters = game.update_counters()



while INTRO:
    game.characters.update()
    game.items.update()
    INTRO = game.intro_2()
    for event in pygame.event.get():
        if f.exit_game(event):
            INTRO = False
            RUN = False
    pygame.display.update()
    clock.tick(FPS)

while RUN:
    # update
    game.update_sprites()
    if not game.is_motion():
        # обновляет счётчики, если у героя закончился действия, то ход переходит к следующему герою
        counters = game.update_counters()

        # добавляет монстров каждую волну
        if counters.wave:
            game._init_monsters_wave()
        game.hero_actions()
        game.monster_actions()

    for event in pygame.event.get():
        if f.exit_game(event):
            RUN = False
        # replay
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            RUN = True
            GAME_OVER = False
            game = Game(screen=screen, map_=MAP, heroes=HEROES, monsters=MONSTERS, items=ITEMS)

    # GAME_OVER
    if game.all_heroes_dead():
        GAME_OVER = True

    if game.monster_waves_counter >= 30 and not game.monsters:
        game.win()
        RUN = False

    # отрисовка экрана
    game.draw()
    if GAME_OVER:
        game.game_over()

    pygame.display.update()
    if counters.turn and game.get_active_character().type == "hero":
        game.update_sprites()
        time.sleep(1)
    clock.tick(FPS)

pygame.quit()
