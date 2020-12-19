""" Рюкзак """

from typing import Optional

import pygame
from pygame import Rect, Surface

import settings as s
from hero import Hero
from text import Text

Game = "Game"


class Menu(Text):
    """ Рюкзак с вещами """
    # noinspection PyUnresolvedReferences
    rect: Rect  # прямоугольник окна на экране (пиксели)
    active_items_id: int  # выбранная вещ в рюкзаке
    hero: Optional[Hero] = None  # ссылка на активного героя

    def __init__(self, screen: Surface):
        super().__init__(screen)
        shift = 90
        window_r = screen.get_rect()
        self.rect = Rect((shift, shift), (window_r.w - shift * 2, window_r.h - shift * 2))
        self.text_x = self.rect.x + 20
        self.text_y = self.rect.y + 50
        self.style = pygame.font.SysFont(self.font, self.size)
        self.active_items_id = 0

    def draw(self) -> None:
        """ рисует окно меню """
        # фон прямоуголник
        pygame.draw.rect(self.screen, s.BLACK, self.rect)
        pygame.draw.rect(self.screen, s.RED_DARK, self.rect, 5)

        # заголовок окна
        xy = (self.rect.centerx, self.rect.y + 10)
        hdr_rect = self.draw_header1_center("MENU", xy)
        # список
        menu_items = [
            "1. single player",
            "2. multiplayer, 2 heroes",
            "3. multiplayer, 3 heroes",
            "4. multiplayer, 4 heroes",
        ]
        lines = []
        for i, line in enumerate(menu_items):
            line_x = self.rect.x + 30
            line_y = self.rect.y + hdr_rect.h + 30 + self.size * i
            lines.append(line)
            self.draw_line(line, line_x, line_y)
