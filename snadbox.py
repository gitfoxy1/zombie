""" game zombie """
# pylint: disable=no-member

import pygame

import functions as f
from games import Game
from hero import Hero
from monster import Monster

FPS = 60
pygame.init()
clock = pygame.time.Clock()
game = Game(map_=2, heroes=0, monsters=0)

# добавим монстра
# random_cell = game.map.random_cell()
monster1 = Monster.little(name="little_monster_1", xy=(0, 0), game=game)
monster1.start_turn()
game.monsters.add(monster1)
game.characters.add(monster1)
game.map.add_characters([monster1])

#  добавить героя
# random_cell = game.map.random_cell()
hero = Hero(name="hero_1", image="hero1.png", xy=(0, 4), game=game)
game.heroes.add(hero)
game.characters.add(hero)
game.map.add_characters([hero])

# отрисовка экрана
map_ = game.map
cell_from = map_.get_cell(monster1.xy)
routes = monster1.random_routes_to_hero(cell_from)
game.draw()
pygame.display.update()
clock.tick(FPS)

RUN = True  # если run = False, тогда выходим из игры
while RUN:
    # обновляет счётчики, если у героя закончился действия, то ход переходит к следующему герою
    counters = game.update_counters()

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
