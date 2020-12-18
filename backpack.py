""" Рюкзак """

from typing import Optional

import pygame
from pygame import Rect

import settings as s
from hero import Hero
from text import Text

Game = "Game"


class Backpack(Text):
    """ Рюкзак с вещами """
    # noinspection PyUnresolvedReferences
    game: Optional[Game] = None  # ссылка на игру
    rect: Rect  # прямоугольник окна на экране (пиксели)
    active_items_id: int  # выбранная вещ в рюкзаке
    hero: Optional[Hero] = None  # ссылка на активного героя

    def __init__(self, game: Game):
        super().__init__(game.screen)
        self.game = game
        shift = 90
        window_r = game.map.rect
        self.rect = Rect((shift, shift), (window_r.w - shift * 2, window_r.h - shift * 2))
        self.color = s.RED_DARK
        self.text_h = 30
        self.text_x = self.rect.x + 20
        self.text_y = self.rect.y + 50
        self.style = pygame.font.SysFont(self.font, self.text_h)
        self.active_items_id = 0

    def draw(self) -> None:
        """ рисует окно рюкзака поверх карты """
        screen = self.game.screen
        self.hero = self.game.get_active_character()
        # фон прямоуголник
        pygame.draw.rect(screen, s.BLACK, self.rect)
        pygame.draw.rect(screen, s.RED_DARK, self.rect, 5)

        # заголовок окна рюкзак
        shift = 10
        xy = (self.rect.centerx, self.rect.y + shift)
        window_hdr_rect = self.draw_header1_center("BACKPACK", xy)
        # заголовок вещей
        xy = (self.rect.x + shift, window_hdr_rect.y + window_hdr_rect.h + shift)
        hdr_rect = self.draw_header2_left("ITEMS:", xy)
        # список вещей
        items_lines = []
        for i in range(len(self.hero.items)):
            item = self.hero.items[i]
            kind = item.kind
            line = "  "
            if self.active_items_id == i:
                line = "> "
            line += f"{i}. {kind}"
            kind_0 = self.hero.items[i].kind_0
            if kind_0 == "cart":  # если патроны
                line += f": {item.count}"
            elif kind_0 in ["armor", "steelweapon"]:
                line += f": {item.strength}"
            line_x = hdr_rect.x
            line_y = hdr_rect.y + hdr_rect.h + shift + self.size * i
            items_lines.append(line)
            self.draw_line(line, line_x, line_y)

    def select_item(self, pressed_key: int) -> None:
        """ кнопками UP/DOWN вибирает предмет в рюкзаке """
        if pressed_key == pygame.K_UP:
            if self.active_items_id > 0:
                self.active_items_id -= 1
        if pressed_key == pygame.K_DOWN:
            hero = self.game.get_active_hero()
            if self.active_items_id >= len(hero.items) - 1:
                pass
            else:
                self.active_items_id += 1

    def item_to_hands(self) -> None:
        """ берём вещь в руки из рюкзака """
        hero = self.game.get_active_hero()
        if not hero.items:
            return
        item_in_hands = hero.item_in_hands
        item_in_backpack = hero.items[self.active_items_id]
        hero.item_in_hands = item_in_backpack
        if item_in_hands:
            hero.items[self.active_items_id] = item_in_hands
        else:
            del hero.items[self.active_items_id]
