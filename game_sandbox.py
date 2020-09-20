# import pygame
# import random
# import os
# import math
#
# import constants as c
# import functions as f
# from character import Hero
# from character import Monster
# from character import Cheater
# from map import Map
# from dashboard import DashboardLeft
# from Items import Digle, Uzi, Kalashnikov
# from backpack import Backpack
#
# debug = 0
# players_count = 5
# # players_count = int(input('сколько будет играть игроков? (от 1 до 4)'))
#
# # screen
# pygame.init()
#
# if debug:
#     screen_w = 900
#     screen_h = 600
#     os.environ['SDL_VIDEO_WINDOW_POS'] = f"1000,0"
#     screen = pygame.display.set_mode((screen_w, screen_h))
# else:
#     os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
#     screen = pygame.display.set_mode()
# screen_w, screen_h = screen.get_size()
# screen_rect = pygame.Rect(0, 0, screen_w, screen_h)
#
# # Персонажи
# charecters = [
#     # Hero('hero_1', 'hero1.png', (-10, -1)),
#     # Hero('hero_2', 'hero2.png', (1, 2)),
#     # Hero('hero_3', 'hero3.png', (1, 5)),
#     Cheater('chiter', 'Cheater.png', (1, 3)),
#     # Hero('hero_4', 'hero4.png', (1, 4)),
# ]
# charecters = charecters[:players_count]
# active_character_id = 0  # активный первый герой charecters[0]
# keyboard_mode = 'map'
#
# # monsters
# monsters = [
#     # Monster('little_monster', 'litel_monster.png', (1, 2), 2, 1),
#     # Monster('big_monster', 'big_monster.png', (1, 4), 1, 1),
#     # Monster('boss_monster_1', 'monster_boss_1.png', (2, 3), 1, 1),
#     # Monster('little_monster', 'litel_monster.png', (0, 3), 2, 1),
# ]
# charecters.extend(monsters)
#
#
# # Карта
# map1 = Map(screen_rect, c.MAP_SANDBOX_NO_WALLS)
# map1.add_charecters(charecters)
# map1.add_items_to_map()
#
#
# # Панель приборов
# dashboard_left = DashboardLeft(screen_rect, map1)
# backpack = Backpack(screen_rect)
#
# # run
# timer = pygame.time.Clock()
# keep_going = True  # если keep_going = False, тогда выходим из игры
# while keep_going:
#     for event in pygame.event.get():  # проверяем любые нажатые кнопки
#         if f.exit_game(event):  # Вйти из игры если нажат знак QUIT или кнопка ESCAPE
#             keep_going = False
#         elif event.type == pygame.KEYDOWN:  # нажата любая кнопка
#             active_character_id, keyboard_mode = f.run_turn(map1, charecters, active_character_id, event, keyboard_mode, screen, backpack, charecters)  # обработка хода героя
#
#     # background
#     screen.fill(c.BLACK)
#     # тестовый рамки панели приборов
#     pygame.draw.rect(screen, c.GREEN, map1.rect, 1)
#     pygame.draw.rect(screen, c.RED, dashboard_left.rect, 10)
#     # pygame.draw.rect(screen, c.BLUE, dashboard_bottom.rect, 1)
#
#     map1.draw(screen)
#
#     for charecter in charecters:
#
#         charecter.draw(screen)
#
#     # for monster in monsters:
#     #     monster.draw(screen)
#
#     dashboard_left.draw(screen, charecters[active_character_id])
#
#     if keyboard_mode == 'backpack':
#         backpack.draw(screen, charecters[active_character_id])
#
#
#
#         # отрисовка экрана
#     pygame.display.update()
#     timer.tick(60)
# pygame.quit()
