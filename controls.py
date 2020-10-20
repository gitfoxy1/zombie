import pygame
import os

import constants as c
from text import Text


class Controls(Text):
    """ Рюкзак """

    def __init__(self, game):
        super().__init__()
        self.game = game
        screen_rect = game.screen_rect()
        # фон картинка
        self.rect = pygame.Rect((screen_rect.x + 90, screen_rect.y + 90), (screen_rect.w - 580, screen_rect.h - 200))
        self.image = pygame.image.load(os.path.join(c.IMAGES_DIR, 'backpack_background.png'))
        self.background = pygame.transform.scale(self.image, (self.rect.w, self.rect.h))

        self.color = c.RED_DARK
        self.text_h = 30
        self.text_x = self.rect.x + 20
        self.text_y = self.rect.y + 50
        self.style = pygame.font.SysFont(self.font, self.text_h)
        self.active_items_id = 0

    def draw(self, screen, hero):
        # фон картинка
        # screen.blit(self.background, self.rect.topleft)
        # # фон прямоуголник
        pygame.draw.rect(screen, c.BLACK, self.rect)
        pygame.draw.rect(screen, c.GREEN, self.rect, 5)

        window_hdr_rect = self.draw_header1_center("THE CLUE", screen, self.rect.centerx, self.rect.y + 10)
        items_hdr_rect = self.draw_header2_left("", screen, self.rect.x + 10,
                                                window_hdr_rect.y + window_hdr_rect.h + 10)

        pattern = '{:<4}{:<10}{}'
        text = [
            'MAP',
            pattern.format(' ', 'up:', 'arrow up'),
            pattern.format(' ', 'down:', 'arrow down'),
            pattern.format(' ', 'right:', 'arrow right'),
            pattern.format(' ', 'left:', 'arrow left'),
            pattern.format(' ', 'drop item:', 'D'),
            pattern.format(' ', 'wear item:', 'W'),
            pattern.format(' ', 'use item:', 'U'),
            'BACKPACK',
            pattern.format(' ', 'backpack:', 'I'),
            pattern.format(' ', 'backpack:', 'I or esc'),
            pattern.format(' ', 'select item:', 'E'),
            'ATTACK',
            pattern.format(' ', 'attack:', 'A + arrow'),
            pattern.format(' ', 'exit from attack:', 'A'),
            'CONTROLS',
            pattern.format(' ', 'control:', 'f1'),
            pattern.format(' ', 'exit from control:', 'f1 or esc'),
            'press alt + f4 to win!!! ;)',
            'goodluck!!!! :D'
        ]
        self.draw_list(text, screen, items_hdr_rect.x, items_hdr_rect.y + items_hdr_rect.h + 10)
