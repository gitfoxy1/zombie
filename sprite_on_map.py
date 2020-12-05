""" спрайт на карте """
import os
from typing import Tuple

import pygame
from pygame import Rect
from pygame import Surface
from pygame.sprite import Sprite

import settings as s

Game = "Game"


class SpriteOnMap(Sprite):
    """ спрайт на карте """

    def __init__(self, image: str, size: Tuple[int, int], game: Game):
        super().__init__()
        self.game: Game = game  # ссылка на игру
        image: str = os.path.join(s.IMAGES_DIR, image)
        surface: Surface = pygame.image.load(image)
        self.image: Surface = pygame.transform.scale(surface, size)  # картинка спрайта
        self.xy: Tuple[int, int] = (-1, -1)  # координаты клетки с этим спрайтом на карте
        self.rect: Rect = self.get_rect()  # прямоугольник спрайта

    def get_rect(self) -> Rect:
        """ помещаем Sprite.rect в центр клетки на экране (пиксели) """
        rect: Rect = self.image.get_rect()
        rect.x = (self.xy[0] * s.CELL_W) + (s.CELL_W / 2 - rect.w / 2)
        rect.y = (self.xy[1] * s.CELL_W) + (s.CELL_W / 2 - rect.h / 2)
        rect.x += self.game.world_shift[0]
        rect.y += self.game.world_shift[1]
        return rect

    def update_rect(self) -> None:
        """ обновим Sprite.rect """
        self.rect = self.get_rect()

    def shift_rect(self, shift_x: int, shift_y: int) -> None:
        """ сдвигаем Sprite.rect """
        rect = self.get_rect()
        rect.x += shift_x
        rect.y += shift_y
        self.rect = rect
