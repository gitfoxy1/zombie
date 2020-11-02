""" Персонажы """

import os

import pygame
from pygame import Rect

import constants as c


class Character(pygame.sprite.Sprite):
    """ Персонаж, класс-родитель для героя и монстра """

    def __init__(self, name, image, cell_xy, game):
        super().__init__()
        self.game = game
        self.type = None
        self.name = name  # имя персонажа
        self.active = False  # герой True=активный False=не активный
        self.cell_xy = list(cell_xy)  # координаты персонажа на карте
        self.scale = 0.9  # размер персонажа относительно ячейки карты
        self.w = int(c.CELL_W * self.scale)  # ширина персонажа по оси x
        self.h = self.w  # высота персонажа по оси y
        self.image = pygame.image.load(os.path.join(c.IMAGES_DIR, image))
        self.image = pygame.transform.scale(self.image, (self.w, self.h))  # лицо
        self.rect = self._get_rect()
        self.items = []
        self.lives = None
        self.item_in_hands = None  # вещь на руках

        self.actions_max = 3  # максимально количество действий героя за один ход игры
        self.actions = 0  # количество действий на данный момент

    def __repr__(self):
        line = f"{self.name}, {self.actions}/{self.actions_max}"
        if self.active:
            line += " active"
        return line

    def _get_rect(self) -> Rect:
        """ return координаны картинки героя в зависимости от ячейки на карте """
        rect = self.image.get_rect()
        # координаты ячкйки на экрана
        cell_x = c.CELL_W * self.cell_xy[0]
        cell_y = c.CELL_W * self.cell_xy[1]
        # координаты героя на экрана, центр героя в центре ячейки
        rect.x = cell_x + c.CELL_W / 2 - self.w / 2
        rect.y = cell_y + c.CELL_W / 2 - self.h / 2
        return rect

    # def draw(self, screen):
    #     """ Рисует персонажа на карте """
    #     cell_x = c.CELL_W * self.xy[0]  # координаты ячкйки на экрана
    #     cell_y = c.CELL_W * self.xy[1]
    #     # координаты героя на экрана, центр героя в центре ячейки
    #     x = cell_x + c.CELL_W / 2 - self.w / 2
    #     y = cell_y + c.CELL_W / 2 - self.h / 2
    #     pic = pygame.transform.scale(self.pic, (self.w, self.h))
    #     screen.blit(pic, (x, y))

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

    def end_turn(self):
        """ ход/turn закончился actions=0, персонаж становится пасивным """
        self.active = False
        self.actions = 0

    def start_turn(self):
        """ персонаж становится активным, начинается его ход/turn """
        self.active = True
        self.actions = self.actions_max
