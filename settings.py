""" константы """

import math
import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
SOUNDS_DIR = os.path.join(PROJECT_DIR, "sounds")
IMAGES_DIR = os.path.join(PROJECT_DIR, "images")

PI = math.pi

SPEED = 100

# размер клетки
CELL_W = 100
CELL_COUNT_X_MAX = 15
CELL_COUNT_Y_MAX = 10

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
WALLS = {"t", "b", "l", "r"}

# звук столкновения героя со стеной
SOUND_PUNCH_TO_WALL = os.path.join(SOUNDS_DIR, "punch_to_wall.wav")

# карты в ascii символах сгенерированая при помощи https://notimetoplay.itch.io/ascii-mapper
# map_ size 15/10 as chars size 32/22
MAP_WITH_ALL_WALLS = """
  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 
 ooooooooooooooooooooooooooooooo
0o.o.o.o.o.o.o.o.o.o.o.o.o.o.o.o
 ooooooooooooooooooooooooooooooo
1o.o.o.o.o.o. . . . . .o.o.o.o.o
 ooooooooooo. . . . . .ooooooooo
2o.o.o.o.o.o. . . . . .o.o.o.o.o
 ooooooooooo. . . . . .ooooooooo
3o.o.o.o.o.o. . . . . .o.o.o.o.o
 ooooooooooo. . . . . .ooooooooo
4o.o.o.o.o.o. . . . . .o.o.o.o.o
 ooooooooooo. . . . . .ooooooooo
5o.o.o.o.o.o. . . . . .o.o.o.o.o
 ooooooooooo. . . . . .ooooooooo
6o.o.o.o.o.o. . . . . .o.o.o.o.o
 ooooooooooo. . . . . .ooooooooo
7o.o. . . . . . . . . . . . .o.o
 ooo. . . . . . . . . . . . .ooo
8o.o. . . . . . . . . . . . .o.o
 ooo. . . . . . . . . . . . .ooo
9o.o. . . . . . . . . . . . .o.o
 ooooooooooooooooooooooooooooooo
"""
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
