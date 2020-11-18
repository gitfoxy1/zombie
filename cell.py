""" клетка карты """
import os
import random
from typing import List, Optional, Set, Tuple, Union

import pygame
from pygame import Rect, Surface

import settings as s
from items import Digle, Uzi, Kalashnikov, LittleCartridge, HeavyCartridge, Fraction, Mastif, \
    Awp, Mozambyk, Knife, Bat


# noinspection PyUnresolvedReferences
class Cell:
    """ клетка карты """
    xy: Tuple[int, int]  # координаты клетки на карте/map
    w: int  # ширина клетки на экране (пиксели) по оси x
    h: int  # высота клетки на экране (пиксели) по оси y
    rect: Optional[Rect] = None  # прямоугольник  клетки на экране (пиксели)
    image: Surface  # картинка клетки
    walls: Set[str]  # стены вокруг клетки: t=top, b=bottom, l=left, r=right
    # noinspection PyUnresolvedReferences
    characters: List[Union["Hero", "Monster"]]  # персонажи которые стоят на этой клетке
    items: List[Union[Digle, Uzi, Kalashnikov, LittleCartridge, HeavyCartridge, Fraction, Mastif,
                      Awp, Mozambyk, Knife, Bat]]  # предметы которые лежат на этой клетке
    status: Set[str]  # состояние клетки: в дыму, в огне

    def __init__(self, xy: Tuple[int, int], walls: set):
        self.xy = xy
        self.w = s.CELL_W
        self.h = self.w
        px = self.xy[0] * self.w
        py = self.xy[1] * self.h
        self.rect = pygame.Rect((px, py), (self.w, self.h))
        # картинки рандом 1..6
        images = [os.path.join(s.IMAGES_DIR, f"map_cell_{i}.png") for i in range(1, 7)]
        self.image = pygame.image.load(random.choice(images))
        self.walls = set(walls)
        self.characters = list()  # hero, monster
        self.items = list()
        # self.status = set()  # todo fire, smoke
        self.rikoshet = pygame.mixer.Sound(os.path.join(s.SOUNDS_DIR, "rikoshet.wav"))  # todo play

    def __repr__(self) -> str:
        msg = f"xy:{self.xy[0]},{self.xy[1]} "
        characters = [str(o) for o in self.characters]
        msg += ", ".join(characters)
        return msg

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

    def get_character(self) -> Optional["Character"]:
        """ return первого персонажа в этой клетке """
        character = [o for o in self.characters]
        if not character:
            return None
        return character[0]

    def get_hero(self) -> Optional["Hero"]:
        """ return первого героя в этой клетке """
        hero = [o for o in self.characters if o.type == "hero"]
        if not hero:
            return None
        return hero[0]

    def get_monster(self) -> Optional["Monster"]:
        """ return первого монстра в этой клетке """
        monster = [o for o in self.characters if o.type == "monster"]
        if not monster:
            return None
        return monster[0]
