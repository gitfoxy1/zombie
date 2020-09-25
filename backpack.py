import pygame
import os

import constants as c
from text import Text


class Backpack(Text):
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
        pygame.draw.rect(screen, c.BLUE, self.rect, 5)


        # заголовок окна рюкзак
        window_hdr_rect = self.draw_header1_center("BACKPACK", screen, self.rect.centerx, self.rect.y + 10)
        # заголовок вещей
        items_hdr_rect = self.draw_header2_left("ITEMS:", screen, self.rect.x + 10, window_hdr_rect.y + window_hdr_rect.h + 10)
        # текст
        lines = []
        for i in range(len(hero.items)):
            line = i
            if hero.items[i].kind_0 == 'cart':  # если патроны
                line = f"{line}. {hero.items[i].kind}: {hero.items[i].count}"
            elif hero.items[i].kind_0 == 'gun':
                line = f"{line}. {hero.items[i].kind}"
            elif hero.items[i].kind_0 == 'steelweapon':
                line = f"{line}. {hero.items[i].kind}: {hero.items[i].strength}"
            elif hero.items[i].kind_0 == 'armor':
                line = f"{line}. {hero.items[i].kind}: {hero.items[i].strength}"
            else:
                raise NotImplementedError(f"neizvestnij predmet: {hero.items[i]}")  # todo udalit' kogda budut vse vidi oruzhja
            if self.active_items_id == i:
                line = f'{line} {"    <"}'
            lines.append(line)
        self.draw_list(lines, screen, items_hdr_rect.x, items_hdr_rect.y + items_hdr_rect.h + 10)

    def select_item(self, pressed_key):
        """ кнопками UP/DOWN вибираем предмет в рюкзаке """
        if pressed_key == pygame.K_UP:
            if self.active_items_id > 0:
                self.active_items_id -= 1
        if pressed_key == pygame.K_DOWN:
            hero = self.game.get_active_character()
            if self.active_items_id >= len(hero.items) - 1:
                pass
            else:
                self.active_items_id += 1

    def clear_item_id(self):
        self.active_items_id = 0

    def item_to_hands(self):
        """ берём вещь в руки из рюкзака """
        hero = self.game.get_active_character()
        item_in_hands = hero.item_in_hands
        item_in_backpack = hero.items[self.active_items_id]
        hero.item_in_hands = item_in_backpack
        hero.items[self.active_items_id] = item_in_hands
