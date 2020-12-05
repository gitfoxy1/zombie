""" константы """

import os
import random

SCREEN_CELLS_W = 5
SCREEN_CELLS_H = 5
CELL_W = 100  # размер клетки
DASHBOARD_W = 300
SPEED = 10

# цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
RED_DARK = (129, 18, 18)
GREY = (120, 120, 120)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
COLORS = {
    "black": BLACK,
    "white": WHITE,
    "red": RED,
    "red_dark": RED_DARK,
    "grey": GREY,
    "blue": BLUE,
    "green": GREEN,
    "yellow": YELLOW,
}

# стены клетки: t=top, b=bottom, l=left, r=right
WALLS = {"up", "down", "left", "right"}

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
# картинки
IMAGES_DIR = os.path.join(PROJECT_DIR, "images")
I_MAP = {
    "map": os.path.join(IMAGES_DIR, "map.png"),
}
I_CELLS = [
    os.path.join(IMAGES_DIR, f"map_cell_1.png"),
    os.path.join(IMAGES_DIR, f"map_cell_2.png"),
    os.path.join(IMAGES_DIR, f"map_cell_3.png"),
    os.path.join(IMAGES_DIR, f"map_cell_4.png"),
    os.path.join(IMAGES_DIR, f"map_cell_5.png"),
    os.path.join(IMAGES_DIR, f"map_cell_6.png"),
]

# звуки
SOUNDS_DIR = os.path.join(PROJECT_DIR, "sounds")
S_BACKGROUND = os.path.join(SOUNDS_DIR, "background.wav")
S_GAME_OVER = os.path.join(SOUNDS_DIR, "game_over.wav")
S_FOOTSTEPS_HERO = os.path.join(SOUNDS_DIR, "footsteps_hero.wav")
S_FOOTSTEPS_MONSTER = os.path.join(SOUNDS_DIR, "footsteps_monster0.wav")
S_PUNCH_TO_WALL = os.path.join(SOUNDS_DIR, "punch_to_wall.wav")
S_PICK_UP = os.path.join(SOUNDS_DIR, "pick_up.wav")
S_DROP_DOWN = os.path.join(SOUNDS_DIR, "drop_down.wav")
# guns
S_GUN_KALASHNIKOV = os.path.join(SOUNDS_DIR, "gun_kalashnikov1.wav")
S_USE = {
    "U.Z.I.": os.path.join(SOUNDS_DIR, "gun_uzi.wav"),
    "Kalashnikov": os.path.join(SOUNDS_DIR, "gun_kalashnikov.wav"),
    "Digle": os.path.join(SOUNDS_DIR, "gun_digle.wav"),
    "A.W.P": os.path.join(SOUNDS_DIR, "gun_awp.wav"),
    "Mozambyk": os.path.join(SOUNDS_DIR, "gun_mazombyk.wav"),
    "Mastif": os.path.join(SOUNDS_DIR, "gun_mastif.wav"),
    "Knife": random.choice([os.path.join(SOUNDS_DIR, "knife1.wav"),
                            os.path.join(SOUNDS_DIR, "knife1.wav")]),
    "Bat": os.path.join(SOUNDS_DIR, "bat.wav"),
}
S_DAMAGE = {
    "kick": random.choice([os.path.join(SOUNDS_DIR, "kick1.wav"),
                           os.path.join(SOUNDS_DIR, "kick2.wav")]),
    "kick_monster1": os.path.join(SOUNDS_DIR, "kick_monster1.wav"),
    "kick_monster2": os.path.join(SOUNDS_DIR, "kick_monster2.wav"),
    "kick_monster3": os.path.join(SOUNDS_DIR, "kick_monster3.wav"),
}
S_BREAKING = {
    "Knife": os.path.join(SOUNDS_DIR, "knife_breaking.wav"),
    "Bat": os.path.join(SOUNDS_DIR, "bat_breaking.wav"),
}
OH = os.path.join(SOUNDS_DIR, "oh.wav")

# карты в ascii символах сгенерированая при помощи https://notimetoplay.itch.io/ascii-mapper
# map_ size 15/10 as chars size 32/22

MAP_1 = """
  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 
 ooooooooooooooooooooooooooooooo
0o. . . . . . . . . . . . . . .o
 o                             o
1o. . . . . . . . . . . . . . .o
 o     ooooooooooooooooooooooooo
2o. . .o. . . . . . . . .o. . .o
 o     o     o           o     o
3o. . .o. . .o. . . . . .o. . .o
 o     ooooooo           ooooo o
4o. . . . . . . . . . . . . . .o
 o     ooo ooooooooooo         o
5o. . .o. . .o. . . .o. . . . .o
 o     o     o       o         o
6o. . .o. . .o. . . .o. . . . .o
 o     o     ooooo   o         o
7o. . .o. . . . .o. . . . . . .o
 o     o         o ooo ooooo   o
8o. . .o. . . . .o. .o.o. . . .o
 o     o         o   o o       o
9o. . .o. . . . .o. .o.o. . . .o
 ooooooooooooooooooooooooooooooo
"""

MAP_SMALL = """
  0 1                           
 ooooo
0o.o.o
 ooooo
1o.o.o
 ooooo
"""
MAP_SANDBOX_NO_WALLS = """
  0 1 2 3 4 
 ooooooooooo
0o. . . . .o
 o         o
1o. . . . .o
 o         o
2o. . . . .o
 o         o
3o. . . . .o
 o         o
4o. . . . .o
 ooooooooooo
"""
MAP_SANDBOX = """
  0 1 2 3 4 
 ooooooooooo
0o.o. . . .o
 o o   ooooo
1o. . . . .o
 o         o
2o. .o.o. .o
 ooo o o   o
3o. .o.o. .o
 o   o o   o
4o. .o.o. .o
 ooooooooooo
"""
