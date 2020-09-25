import pygame

import constants as c
from Items import Digle, Uzi, Kalashnikov, LittleCartridge, HeavyCartridge, Fraction, Cartridge

class DashboardLeft:
    """ Левая панель """
    def __init__(self, screen_rect, map):
        self.rect = pygame.Rect(map.rect.topright, (screen_rect.w - map.rect.w, screen_rect.h))
        self.image_x = self.rect.x + 20
        self.image_y = self.rect.y + 20
        self.image_w = 150
        self.font = "consolas"
        self.color = c.RED_DARK
        self.text_h = 20
        self.text_x = self.rect.x + 20
        self.text_y = self.image_y + self.image_w + self.text_h
        self.style = pygame.font.SysFont(self.font, self.text_h)

    def draw(self, screen, hero):
        # фон
        pygame.draw.rect(screen, c.BLACK, self.rect)

        # лицо
        pic = pygame.transform.scale(hero.image, (self.image_w, self.image_w))
        screen.blit(pic, (self.image_x, self.image_y))
        # in hands
        in_hands = hero.item_in_hands
        if in_hands:
            in_hands = hero.item_in_hands.kind
        armor = hero.armor
        strength = 0
        if armor:
            armor = hero.armor.kind
            strength = hero.armor.strength

        # ищем патроны для оружия в рюкзаке героя
        cart_count = 0
        # cart_count_str = ''
        if in_hands:
            for item_i in hero.items:
                # ищем патроны нужного типа в рюкзаке
                if hero.item_in_hands.kind_0 == 'gun':  # если в руках оружие
                    if item_i.kind == hero.item_in_hands.cartridge_kind:  # если патроны подходят к оружию
                        cart_count = item_i.count
                        # cart_count_str = f'{cart_count}'
                        break

                elif hero.item_in_hands.kind_0 == 'cart':  # если в руках патроны или гранаты
                    cart_count = hero.item_in_hands.count  # будем писать кол. патронов которые мы держим
                    break
                # cart_count_str = cart_count

        # текст
        rows = ["{:<9} {}".format("Name:", hero.name),
                "{:<9} {}".format("Health:", hero.lives + strength),
                "{:<9} {}".format("Actions:", hero.actions),
                "{:<9} {}, {}".format("In hands:", in_hands, cart_count),
                "{:<9} {}".format("Items in backpack:", len(hero.items)),
                "{:<9} {}, {}".format("Armor:", armor, strength)]
        #         "{}".format("Items:")]
        # if hero.items:  # если в рюкзаке есть вещи
        #     for item in hero.items:
        #         if item.kind_0 == 'cart':  # если патроны
        #             rows.append("{} {}".format(item.kind, item.count))
        #         elif item.kind_0 == 'gun':
        #             rows.append(item.kind)




                # else:
                #     assert('in list items not this item')






        for cart_count_str in range(len(rows)):
            row = rows[cart_count_str]
            text = self.style.render(row, True, self.color)
            xy = (self.text_x, self.text_y + self.text_h * cart_count_str)
            screen.blit(text, xy)


class DashboardBottom:
    """ Нижняя панель """
    def __init__(self, screen_rect, map):
        self.rect = pygame.Rect(map.rect.bottomleft, (map.rect.w, screen_rect.h - map.rect.h))

    def draw(self):
        pass