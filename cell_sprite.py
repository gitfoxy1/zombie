""" клетка карты """
import os
import random

import pygame
from pygame import Rect, Surface
from pygame.sprite import Sprite

import settings as s


# noinspection PyUnresolvedReferences
class CellSprite(Sprite):
    """ клетка карты """

    def __init__(self, rect: "Rect"):
        super().__init__()
        images = [os.path.join(s.IMAGES_DIR, f"map_cell_{i}.png") for i in range(1, 7)]
        image = random.choice(images)
        self.image: Surface = pygame.image.load(image)  # картинка спрайта
        self.rect: Rect = rect
