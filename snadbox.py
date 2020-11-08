""" game zombie """
# pylint: disable=no-member

import pygame

import functions as f
from games import Game
from hero import Hero
from monster import Monster

FPS = 60
pygame.init()
# screen = pygame.display.set_mode([100, 100])
clock = pygame.time.Clock()
game = Game(heroes=0, monsters=0, map_id=2)

# добавим монстра
random_cell = game.map.random_cell()
monster1 = Monster.little(name="little_monster_1", xy=random_cell.xy, game=game)
monster1.start_turn()
game.monsters.add(monster1)
game.characters.add(monster1)
game.map.add_characters([monster1])

#  добавить героя
random_cell = game.map.random_cell()
hero = Hero(name="hero_1", image="hero1.png", xy=random_cell.xy, game=game)
game.heroes.add(hero)
game.characters.add(hero)
game.map.add_characters([hero])


RUN = True  # если run = False, тогда выходим из игры
while RUN:

    # обновляет счётчики, если у героя закончился действия, то ход переходит к следующему герою
    counters = game.update_counters()
    game.monster_actions()

    for event in pygame.event.get():  # проверяет любые нажатые кнопки
        if f.exit_game(event):  # Вйти из игры если нажат знак QUIT или кнопка ESCAPE
            RUN = False
    # отрисовка экрана
    game.draw()
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
