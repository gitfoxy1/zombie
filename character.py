""" Персонажы """

import os
from typing import Optional, Tuple

import pygame
from pygame import Surface
from pygame.sprite import Sprite
from pygame import Rect

import settings as s
from cell import Cell
from sprite_on_map import SpriteOnMap

Game = "Game"


class Character(SpriteOnMap):
    """ Персонаж, класс-родитель для героя и монстра """
    # noinspection PyUnresolvedReferences
    type: Optional[str] = ""  # тип персонажа: "hero", "monster"
    name: str = ""  # имя персонажа
    active: bool = False  # True= персонаж активный, может действовать; False= не активный, ждёт

    def __init__(self, name: str, image: str, xy: Tuple[int, int], game: Game):
        self.game: Game = game  # ссылка на игру

        scale = 0.9
        width = int(s.CELL_W * scale)
        size = (width, width)
        super().__init__(image, size)
        self.xy = xy
        self.rect = self.get_rect()  # Sprite.rect

        self.type = None
        self.name = name
        self.active = False
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

    def get_rect(self) -> Rect:
        """ Sprite.rect на экране (пиксели) в центр клетки """
        rect: Rect = self.image.get_rect()
        # координаты клетки на экрана в пикселях
        px = s.CELL_W * self.xy[0]
        py = s.CELL_W * self.xy[1]
        # координаты героя на экрана, центр героя в центре клетки
        rect.x = px + s.CELL_W / 2 - rect.w / 2
        rect.y = py + s.CELL_W / 2 - rect.h / 2
        return rect

    def update(self):
        """ update """
        speed = s.SPEED
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
