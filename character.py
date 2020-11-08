""" Персонажы """

import os
from typing import Optional, List

import pygame
from pygame import Rect, Surface

import constants as c


class Character(pygame.sprite.Sprite):
    """ Персонаж, класс-родитель для героя и монстра """
    # noinspection PyUnresolvedReferences
    game: Optional["Game"] = None  # ссылка на игру
    type: Optional[str]  # тип персонажа: "hero", "monster"
    name: str  # имя персонажа
    active: bool  # True= персонаж активный, может действовать; False= не активный, ждёт
    xy: List[int]  # координаты персонажа на карте/map
    scale: float  # размер персонажа относительно клетки карты
    w: int  # ширина персонажа на экране (пиксели) по оси x
    h: int  # высота персонажа на экране (пиксели) по оси y
    image: Surface  # картинка персонажа

    # noinspection PyUnresolvedReferences
    def __init__(self, name: str, image: str, xy: list, game: "Game"):
        super().__init__()
        self.game = game
        self.type = None
        self.name = name
        self.active = False
        self.xy = list(xy)  # todo list() не нужен
        self.scale = 0.9
        self.w = int(c.CELL_W * self.scale)
        self.h = self.w
        image = pygame.image.load(os.path.join(c.IMAGES_DIR, image))
        self.image = pygame.transform.scale(image, (self.w, self.h))
        self.rect = self._rect_in_cell_center()
        self.items = []
        self.lives = None
        self.item_in_hands = None  # вещь на руках

        self.actions_max = 3  # максимально количество действий героя за один ход игры
        self.actions = 0  # количество действий на данный момент

    def __repr__(self) -> str:
        line = f"{self.name}, {self.actions}/{self.actions_max}"
        if self.active:
            line += " active"
        return line

    def _rect_in_cell_center(self) -> Rect:
        """ устанавливает прямоугольник героя на экране (пиксели) в центре клетки """
        rect = self.image.get_rect()
        # координаты клетки на экрана в пикселях
        px = c.CELL_W * self.xy[0]
        py = c.CELL_W * self.xy[1]
        # координаты героя на экрана, центр героя в центре клетки
        rect.x = px + c.CELL_W / 2 - self.w / 2
        rect.y = py + c.CELL_W / 2 - self.h / 2
        return rect

    def death(self) -> None:
        """ Персонаж умирает """
        # ищет героя на карте
        for cell in self.game.map.cells:
            if self in cell.characters:
                # удаляет героя с карты
                cell.characters.remove(self)
                # вещи героя сбрасывает на карту
                for item in self.items:
                    cell.items.append(item)
                break
        # удаляет героя из игры
        self.game.characters.remove(self)
        self.game.heroes.remove(self)
        self.game.monsters.remove(self)

    def end_turn(self) -> None:
        """ ход/turn закончился actions=0, персонаж становится пасивным """
        self.active = False
        self.actions = 0

    def start_turn(self) -> None:
        """ персонаж становится активным, начинается его ход/turn """
        self.active = True
        self.actions = self.actions_max
