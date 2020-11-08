""" клетка карты """
import os
import random
from typing import List, Set, Tuple, Union

import pygame
from pygame import Rect, Surface

import constants as c
from items import Digle, Uzi, Kalashnikov, LittleCartridge, HeavyCartridge, Fraction, Mastif, \
    Awp, Mozambyk, Knife, Bat


class Cell:
    """ клетка карты """
    xy: Tuple[int, int]  # координаты клетки на карте/map
    w: int  # ширина клетки на экране (пиксели) по оси x
    h: int  # высота клетки на экране (пиксели) по оси y
    rect: Rect  # прямоугольник  клетки на экране (пиксели)
    image: Surface  # картинка клетки
    walls: Set[str]  # стены вокруг клетки: t=top, b=bottom, l=left, r=right
    # noinspection PyUnresolvedReferences
    characters: List[Union["Hero", "Monster"]]  # персонажи которые стоят на этой клетке
    items: List[Union[Digle, Uzi, Kalashnikov, LittleCartridge, HeavyCartridge, Fraction, Mastif,
                      Awp, Mozambyk, Knife, Bat]]  # предметы которые лежат на этой клетке
    status: Set[str]  # состояние клетки: в дыму, в огне

    def __init__(self, xy: Tuple[int, int], walls: set):
        self.xy = xy
        self.w = c.CELL_W
        self.h = self.w
        x_screen = self.xy[0] * self.w
        y_screen = self.xy[1] * self.h
        self.rect = pygame.Rect((x_screen, y_screen), (self.w, self.h))
        # картинки рандом 1..6
        images = [os.path.join(c.IMAGES_DIR, f"map_cell_{i}.png") for i in range(1, 7)]
        self.image = pygame.image.load(random.choice(images))
        self.walls = set(walls)
        self.characters = list()  # hero, monster
        self.items = list()
        # self.status = set()  # todo fire, smoke
        self.rikoshet = pygame.mixer.Sound(os.path.join(c.SOUNDS_DIR, "rikoshet.wav"))  # todo play

    def __repr__(self) -> str:
        return f"xy:{self.xy[0]},{self.xy[1]}"

    def top_left(self, shift: float = 0) -> Tuple[int, int]:
        """ return координаты экрана, верхний левый угол """
        screen_x = int(self.xy[0] * self.w)
        screen_y = int(self.xy[1] * self.h)
        if shift:
            screen_x += shift
            screen_y += shift
        return screen_x, screen_y

    def top_right(self, shift: float = 0) -> Tuple[int, int]:
        """ return координаты экрана, верхний правый угол """
        screen_x = int(self.xy[0] * self.w + self.w)
        screen_y = int(self.xy[1] * self.h)
        if shift:
            screen_x -= shift
            screen_y += shift
        return screen_x, screen_y

    def bottom_left(self, shift: float = 0) -> Tuple[int, int]:
        """ return координаты экрана, нижний левый угол """
        screen_x = int(self.xy[0] * self.w)
        screen_y = int(self.xy[1] * self.h + self.h)
        if shift:
            screen_x += shift
            screen_y -= shift
        return screen_x, screen_y

    def bottom_right(self, shift: float = 0) -> Tuple[int, int]:
        """ return координаты экрана, нижний правый угол """
        screen_x = int(self.xy[0] * self.w + self.w)
        screen_y = int(self.xy[1] * self.h + self.h)
        if shift:
            screen_x -= shift
            screen_y -= shift
        return screen_x, screen_y

    def center(self) -> Tuple[int, int]:
        """ return координаты экрана, центр """
        screen_x = int(self.xy[0] * self.w + round(self.w / 2, 0))
        screen_y = int(self.xy[1] * self.h + round(self.h / 2, 0))
        return screen_x, screen_y
