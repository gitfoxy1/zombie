""" Персонажы """

import os
from typing import Optional, Tuple

import pygame
from pygame import Surface
from pygame.sprite import Sprite
from pygame import Rect

import constants as c
from cell import Cell


class Character(Sprite):
    """ Персонаж, класс-родитель для героя и монстра """
    # noinspection PyUnresolvedReferences
    game: Optional["Game"] = None  # ссылка на игру
    type: Optional[str] = ""  # тип персонажа: "hero", "monster"
    name: str = ""  # имя персонажа
    active: bool = False  # True= персонаж активный, может действовать; False= не активный, ждёт
    xy: Optional[Tuple[int, int]] = None  # координаты персонажа на карте/map
    rect: Optional[Rect] = None
    scale: float = 0.0  # размер персонажа относительно клетки карты
    w: int = 0  # ширина персонажа на экране (пиксели) по оси x
    h: int = 0  # высота персонажа на экране (пиксели) по оси y
    image: Optional[Surface] = None  # картинка персонажа

    # noinspection PyUnresolvedReferences
    def __init__(self, name: str, image: str, xy: Tuple[int, int], game: "Game"):
        super().__init__()
        self.game = game
        self.type = None
        self.name = name
        self.active = False
        self.xy = xy
        self.scale = 0.9
        self.w = int(c.CELL_W * self.scale)
        self.h = self.w
        image = pygame.image.load(os.path.join(c.IMAGES_DIR, image))
        self.image = pygame.transform.scale(image, (self.w, self.h))
        self.update_rect()  # attribute in Sprite
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

    def get_cell(self) -> Cell:
        """ return клетку в которой находится персонаж """
        cell = self.game.map.get_cell(self.xy)
        return cell

    def move_to_cell(self, cell_to: Cell) -> None:
        """ Передвижение персонажа в клету"""
        # найдём клетку в которой находится персонаж
        map_ = self.game.map
        cell_from = map_.get_cell(self.xy)

        # перемещаеме персонаж в другую клетку на карте
        self.xy = cell_to.xy
        cell_from.characters.remove(self)  # удаляем из сатрой клетки
        cell_to.characters.append(self)  # добавляем в новую клетку
        # self.update_rect()  # обновили на экране

    def update_rect(self) -> None:
        """ обновляем Sprite.rect на экране (пиксели) в центр клетки """
        rect: Rect = self.image.get_rect()
        # координаты клетки на экрана в пикселях
        px = c.CELL_W * self.xy[0]
        py = c.CELL_W * self.xy[1]
        # координаты героя на экрана, центр героя в центре клетки
        rect.x = px + c.CELL_W / 2 - self.w / 2
        rect.y = py + c.CELL_W / 2 - self.h / 2
        self.rect = rect

    def update(self):
        """ update """
        speed = 15
        cell = self.game.map.get_cell(self.xy)
        # x
        diff_x = abs(self.rect.centerx - cell.rect.centerx)
        diff_x = min(speed, diff_x)
        if diff_x:
            if self.rect.centerx > cell.rect.centerx:
                self.rect.centerx -= diff_x
            elif self.rect.centerx < cell.rect.centerx:
                self.rect.centerx += diff_x
        # y
        diff_y = abs(self.rect.centery - cell.rect.centery)
        diff_y = min(speed, diff_y)
        if diff_y:
            if self.rect.centery > cell.rect.centery:
                self.rect.centery -= diff_y
            elif self.rect.centery < cell.rect.centery:
                self.rect.centery += diff_y


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
