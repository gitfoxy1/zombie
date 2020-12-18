""" клетка карты """
import random
from typing import List, Optional, Set, Tuple, Union

from pygame import Rect

import settings as s
from items import Digle, Uzi, Kalashnikov, Cartridge, HeavyCartridge, Fraction, Mastif, \
    Awp, Mozambyk, Knife, Bat
from sprite_on_map import SpriteOnMap

Game = "Game"


# noinspection PyUnresolvedReferences
class Cell(SpriteOnMap):
    """ клетка карты """

    characters: List[Union["Hero", "Monster"]]  # персонажи которые стоят на этой клетке
    items: List[Union[Digle, Uzi, Kalashnikov, Cartridge, HeavyCartridge, Fraction, Mastif,
                      Awp, Mozambyk, Knife, Bat]]  # предметы которые лежат на этой клетке
    status: Set[str]  # состояние клетки: в дыму, в огне

    def __init__(self, xy: Tuple[int, int], walls: set, game: Game):
        image = random.choice(s.I_CELLS)  # картинки рандом 1..6
        super().__init__(image=image, size=(100, 100), game=game)
        self.xy = xy  # координаты клетки на карте/map
        self.update_rect()
        self.walls: set = set(walls)  # стены вокруг клетки: t=top, b=bottom, l=left, r=right
        self.characters = list()  # hero, monster
        self.items = list()

    def __repr__(self) -> str:
        msg = f"xy:{self.xy[0]},{self.xy[1]}"
        characters = [o.name for o in self.characters]
        if characters:
            characters_ = ",".join(characters)
            msg += f" characters: {characters_}"
        return msg

    def top_left(self, shift: float = 0) -> Tuple[int, int]:
        """ return координаты экрана, верхний левый угол """
        screen_x = int(self.xy[0] * self.rect.width)
        screen_y = int(self.xy[1] * self.rect.height)
        if shift:
            screen_x += shift
            screen_y += shift
        return screen_x, screen_y

    def top_right(self, shift: float = 0) -> Tuple[int, int]:
        """ return координаты экрана, верхний правый угол """
        screen_x = int(self.xy[0] * self.rect.width + self.rect.width)
        screen_y = int(self.xy[1] * self.rect.height)
        if shift:
            screen_x -= shift
            screen_y += shift
        return screen_x, screen_y

    def bottom_left(self, rect: Rect, shift: float = 0) -> Tuple[int, int]:
        """ return координаты экрана, нижний левый угол """
        screen_x = int(self.xy[0] * self.rect.width)
        screen_y = int(self.xy[1] * self.rect.height + self.rect.height) - rect.height
        if shift:
            screen_x += shift
            screen_y -= shift
        return screen_x, screen_y

    def bottom_right(self, rect: Rect, shift: float = 0) -> Tuple[int, int]:
        """ return координаты экрана, нижний правый угол """
        screen_x = int(self.xy[0] * self.rect.width + self.rect.width) - rect.width
        screen_y = int(self.xy[1] * self.rect.height + self.rect.height) - rect.height
        if shift:
            screen_x -= shift
            screen_y -= shift
        return screen_x, screen_y

    def center(self) -> Tuple[int, int]:
        """ return координаты экрана, центр """
        screen_x = int(self.xy[0] * self.rect.width + round(self.rect.width / 2, 0))
        screen_y = int(self.xy[1] * self.rect.height + round(self.rect.height / 2, 0))
        return screen_x, screen_y

    def get_character(self) -> Optional["Character"]:
        """ return последнего/верхнего персонажа в этой клетке """
        characters = [o for o in self.characters]
        if not characters:
            return None
        return characters[-1]

    def get_character_without(self, without_character: "Character") -> Optional["Character"]:
        """ return последнего/верхнего персонажа в этой клетке, без without_character """
        characters = [o for o in self.characters]
        if not characters:
            return None
        characters = [o for o in characters if o != without_character]
        if not characters:
            return None
        return characters[-1]

    def get_hero(self) -> Optional["Hero"]:
        """ return последнего/верхнего героя в этой клетке """
        hero = [o for o in self.characters if o.type == "hero"]
        if not hero:
            return None
        return hero[-1]

    def get_monster(self) -> Optional["Monster"]:
        """ return последнего/верхнего монстра в этой клетке """
        monster = [o for o in self.characters if o.type == "monster"]
        if not monster:
            return None
        return monster[-1]

    def has_wall(self, direction: str) -> bool:
        """ True если есть срена в направлении движения """
        if direction in self.walls:
            return True
        return False

    def is_hero(self) -> bool:
        """ True если есть герой на этой клетке """
        if self.get_hero():
            return True
        return False

    def is_monster(self) -> bool:
        """ True если есть монстр на этой клетке """
        if self.get_monster():
            return True
        return False

    def pop_item(self) -> Optional["Item"]:
        """ return вещь из клетки карты, удаляет из списка """
        if not self.items:
            return
        item = self.items.pop()
        item.xy = (-1, -1)
        item.update_rect()
        return item

    def append_item(self, item: "Item") -> None:
        """ кладём вещь на клетку карты """
        item.xy = self.xy
        item.update_rect()
        self.items.append(item)
