""" Help, назначение клавиш """
import pygame
from pygame import Rect

import settings as s
from text import Text

Game = "Game"


class Controls(Text):
    """ Help, назначение клавиш """

    # noinspection PyUnresolvedReferences
    def __init__(self, game: Game):
        super().__init__(game.screen)
        self.game = game
        shift = 90
        window_r = game.screen.get_rect()
        self.rect = Rect((shift, shift), (window_r.w - shift * 2, window_r.h - shift * 2))
        self.color = s.RED_DARK
        self.text_h = 30
        self.text_x = self.rect.x + 20
        self.text_y = self.rect.y + 50
        self.style = pygame.font.SysFont(self.font, self.text_h)
        self.active_items_id = 0

    def draw(self):
        """ рисует окно Help поверх карты """
        # фон прямоуголник
        pygame.draw.rect(self.screen, s.BLACK, self.rect)
        pygame.draw.rect(self.screen, s.RED_DARK, self.rect, 5)

        xy = (self.rect.centerx, self.rect.y + 10)
        window_hdr_rect = self.draw_header1_center("Controls", xy)
        xy = (self.rect.x + 10, window_hdr_rect.y + window_hdr_rect.h + 10)
        items_hdr_rect = self.draw_header2_left("", xy)

        pattern = "{:<4}{:<25}{}"
        text = [
            # "MAP",
            pattern.format(" ", "up:", "arrow up"),
            pattern.format(" ", "down:", "arrow down"),
            pattern.format(" ", "right:", "arrow right"),
            pattern.format(" ", "left:", "arrow left"),
            pattern.format(" ", "attack", "A then arrow"),
            pattern.format(" ", "pick up item:", "E"),
            pattern.format(" ", "drop item:", "D"),
            pattern.format(" ", "wear item:", "W"),
            pattern.format(" ", "use item:", "U"),
            pattern.format(" ", "exit from game:", "ALT + F4"),
            pattern.format(" ", "enter to backpack:", "I"),
            pattern.format(" ", "select item in backpack:", "ENTER"),
            pattern.format(" ", "replay:", "R"),
            pattern.format(" ", "control:", "F1"),
            "",
            "goodluck!!!! :D"
        ]
        self.draw_list(text, items_hdr_rect.x, items_hdr_rect.y + items_hdr_rect.h + 10)
