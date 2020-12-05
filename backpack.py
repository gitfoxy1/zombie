""" Рюкзак """

from typing import Optional

import pygame
from pygame import Rect, Surface

import settings as s
from text import Text

Game = "Game"


class Backpack(Text):
    """ Рюкзак с вещами """
    # noinspection PyUnresolvedReferences
    game: Optional[Game] = None  # ссылка на игру
    rect: Rect  # прямоугольник окна на экране (пиксели)
    active_items_id: int  # выбранная вещ в рюкзаке

    # noinspection PyUnresolvedReferences
    def __init__(self, game: Game):
        super().__init__()
        self.game = game
        screen_r = game.screen.get_rect()
        shift = 80
        self.rect = Rect((shift, shift), (screen_r.w - shift * 2, screen_r.h - shift * 2))
        self.color = s.RED_DARK
        self.text_h = 30
        self.text_x = self.rect.x + 20
        self.text_y = self.rect.y + 50
        self.style = pygame.font.SysFont(self.font, self.text_h)
        self.active_items_id = 0

    # noinspection PyUnresolvedReferences
    def draw(self, screen: Surface, hero: "Hero") -> None:
        """ рисует окно рюкзака поверх карты """
        # фон прямоуголник
        pygame.draw.rect(screen, s.BLACK, self.rect)
        pygame.draw.rect(screen, s.BLUE, self.rect, 5)

        # заголовок окна рюкзак
        xy = (self.rect.centerx, self.rect.y + 10)
        window_hdr_rect = self.draw_header1_center("BACKPACK", screen, xy)
        # заголовок вещей
        xy = (self.rect.x + 10, window_hdr_rect.y + window_hdr_rect.h + 10)
        items_hdr_rect = self.draw_header2_left("ITEMS:", screen, xy)
        # текст
        lines = []
        for i in range(len(hero.items)):
            line = i
            if hero.items[i].kind_0 == "cart":  # если патроны
                line = f"{line}. {hero.items[i].kind}: {hero.items[i].count}"
            elif hero.items[i].kind_0 == "gun":
                line = f"{line}. {hero.items[i].kind}"
            elif hero.items[i].kind_0 == "steelweapon":
                line = f"{line}. {hero.items[i].kind}: {hero.items[i].strength}"
            elif hero.items[i].kind_0 == "armor":
                line = f"{line}. {hero.items[i].kind}: {hero.items[i].strength}"
            elif hero.items[i].kind_0 == "medicine":
                line = f"{line}. {hero.items[i].kind}"
            elif hero.items[i].kind_0 == "backpack":
                line = f"{line}. {hero.items[i].kind}"
            else:
                # todo удалить когда будут все виды оружия
                raise NotImplementedError(f"neizvestnij predmet: {hero.items[i]}")
            if self.active_items_id == i:
                line += "     <"
            lines.append(line)
        self.draw_list(lines, screen, items_hdr_rect.x, items_hdr_rect.y + items_hdr_rect.h + 10)

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
        item_in_hands = hero.item_in_hands
        item_in_backpack = hero.items[self.active_items_id]
        hero.item_in_hands = item_in_backpack
        if item_in_hands:
            hero.items[self.active_items_id] = item_in_hands
        else:
            del hero.items[self.active_items_id]
