""" Левая панель """
import pygame
from pygame import Rect

import settings as s
from map import Map


class DashboardLeft:
    """ Левая панель """

    def __init__(self, screen_rect: Rect, map_: Map):
        self.rect = pygame.Rect(map_.rect.topright, (screen_rect.w - map_.rect.w, screen_rect.h))
        self.image_x = self.rect.x + 20
        self.image_y = self.rect.y + 20
        self.image_w = 150
        self.font = "consolas"
        self.color = s.RED_DARK
        self.text_h = 20
        self.text_x = self.rect.x + 20
        self.text_y = self.image_y + self.image_w + self.text_h
        self.style = pygame.font.SysFont(self.font, self.text_h)

    def draw(self, screen, hero):
        """ рисует панель в левой части экрана """
        # фон
        pygame.draw.rect(screen, s.BLACK, self.rect)

        # лицо
        pic = pygame.transform.scale(hero.image, (self.image_w, self.image_w))
        screen.blit(pic, (self.image_x, self.image_y))

        # текст
        rows1 = [
            "{:<9} {}".format("Name:", hero.name),
            "{:<9} {}".format("Health:", hero.lives),
            "{:<9} {}".format("Actions:", hero.actions),
        ]

        rows2 = list()
        if hero.type == "hero":
            # in hands
            in_hands = hero.item_in_hands
            if in_hands:
                in_hands = hero.item_in_hands.kind
            armor = hero.armor
            strength = 0
            if armor:
                armor = hero.armor.kind
                strength = hero.armor.strength

            # ищет патроны для оружия в рюкзаке героя
            cart_count = 0
            # cart_count_str = ""
            if in_hands:
                for item_i in hero.items:
                    # ищет патроны нужного типа в рюкзаке
                    if hero.item_in_hands.kind_0 == "gun":  # если в руках оружие
                        # если патроны подходят к оружи.
                        if item_i.kind == hero.item_in_hands.cartridge_kind:
                            cart_count = item_i.count
                            # cart_count_str = f"{cart_count}"
                            break

                    # если в руках патроны или гранаты
                    elif hero.item_in_hands.kind_0 == "cart":
                        # будет писать кол. патронов которые мы держим
                        cart_count = hero.item_in_hands.count
                        break
                    # cart_count_str = cart_count

            # текст
            rows2 = ["{:<9} {}".format("Strength:", strength),
                     "{:<9} {}, {}".format("In hands:", in_hands, cart_count),
                     "{:<9} {}".format("Items in backpack:", len(hero.items)),
                     "{:<9} {}, {}".format("Armor:", armor, strength)]

        # рисует текст на дашборде
        rows = rows1 + rows2
        for i, row in enumerate(rows):
            text = self.style.render(row, True, self.color)
            xy = (self.text_x, self.text_y + self.text_h * i)
            screen.blit(text, xy)


class DashboardBottom:
    """ Нижняя панель """

    def __init__(self, screen_rect, map_):
        self.rect = pygame.Rect(map_.rect.bottomleft, (map_.rect.w, screen_rect.h - map_.rect.h))

    def draw(self):
        """ рисует панель внизу экрана """
