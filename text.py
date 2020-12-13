""" текст """
from typing import Tuple

import pygame
from pygame import Surface

import settings as s


class Text:
    """ текст """

    def __init__(self, screen: Surface):
        self.screen: Surface = screen
        self.color = s.RED_DARK
        self.size: int = 30
        self.font: str = "consolas"

    def draw_header1_center(self, text: str, xy: Tuple[int, int]):
        """ Пишет загловок в центре """
        size = int(self.size * 2)
        font = pygame.font.SysFont(self.font, size)
        font.set_underline(True)
        font.set_bold(True)
        render = font.render(text, True, self.color)
        text_rect = render.get_rect()
        xy_ = (xy[0] - text_rect.centerx, xy[1])
        self.screen.blit(render, xy_)
        box_rect = pygame.Rect(xy_, text_rect.size)
        return box_rect

    def draw_header2_left(self, text: str, xy: Tuple[int, int]):
        """ Пишет загловок слела """
        size = int(self.size * 1.5)
        font = pygame.font.SysFont(self.font, size)
        font.set_underline(True)
        font.set_bold(True)
        render = font.render(text, True, self.color)
        text_rect = render.get_rect()
        xy = (xy[0] + size * 0.2, xy[1])
        self.screen.blit(render, xy)
        box_rect = pygame.Rect(xy, text_rect.size)
        return box_rect

    def draw_line(self, text: str, x: int, y: int) -> None:
        """ Пишет список строк """
        font = pygame.font.SysFont(self.font, self.size)
        font.set_underline(False)
        surface = font.render(text, True, self.color)
        self.screen.blit(surface, (x, y))

    def draw_list(self, lines, x, y):
        """ Пишет список строк """
        size = self.size
        font = pygame.font.SysFont(self.font, size)
        font.set_underline(False)
        font.set_bold(False)
        box_w = int()
        box_h = int()
        for i, text in enumerate(lines):
            render = font.render(text, True, self.color)
            text_rect = render.get_rect()
            y_i = y + size * i
            xy = (x, y_i)
            self.screen.blit(render, xy)
            box_w = max(box_w, text_rect.w)
            box_h = y_i + text_rect.h
            print()
        box_rect = pygame.Rect((x, y), (box_w, box_h - y))
        return box_rect
