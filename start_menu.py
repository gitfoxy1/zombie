""" Меню, выбор героев для мультиплеера """
import os
import pygame

import settings as s
from text import Text
from pygame import Rect, Surface

Game = "Game"


class StartMenu():
    """ Меню, выбор героев для мультиплеера """

    def __init__(self):
        """  Создаёт меню """
        self.screen = self._init_screen()

        # super().__init__(game.screen)
        # self.game = game
        # shift = 90
        # window_r = game.screen.get_rect()
        # self.rect = Rect((shift, shift), (window_r.w - shift * 2, window_r.h - shift * 2))

    @staticmethod
    def _init_screen() -> Surface:
        """ Создаёт экран игры """
        if s.SCREEN_SIZE[0] and s.SCREEN_SIZE[1]:  # окно
            screen = pygame.display.set_mode((s.SCREEN_SIZE[0], s.SCREEN_SIZE[1]))
        else:
            os.environ["SDL_VIDEO_WINDOW_POS"] = "0,0"  # полноэкранный режим
            screen = pygame.display.set_mode()
        return screen

    def draw(self):
        """ рисует окно Help поверх карты """
        # фон прямоуголник
        pygame.draw.rect(self.screen, s.BLACK, self.rect)
        pygame.draw.rect(self.screen, s.RED_DARK, self.rect, 5)



