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

    def __init__(self, image: str, size: Tuple[int, int]):
        super().__init__()
        image = os.path.join(s.IMAGES_DIR, image)
        image = pygame.image.load(image)
        image = pygame.transform.scale(image, size)
        self.image: Surface = image  # картинка спрайта
        self.xy: Tuple[int, int] = (-1, -1)  # координаты клетки спрайта на карте
        self.rect: Rect = self.image.get_rect()
        self.update_rect()  # прямоугольник спрайта

    def update_rect(self) -> None:
        """ return Sprite.rect на экране (пиксели) в центр клетки карты """
        rect: Rect = self.image.get_rect()
        # координаты клетки на экрана в пикселях
        px = s.CELL_W * self.xy[0]
        py = s.CELL_W * self.xy[1]
        # координаты спрайта на экрана, центр героя в центре клетки
        rect.x = px + s.CELL_W / 2 - rect.w / 2
        rect.y = py + s.CELL_W / 2 - rect.h / 2
        self.rect = rect
