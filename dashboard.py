""" Левая панель """
import pygame

import settings as s

Game = "Game"


class Dashboard:
    """ Левая панель """

    def __init__(self, game: Game):
        self.game = game
        map_rect = game.map.rect
        xy = map_rect.topright
        size = (map_rect.width + s.DASHBOARD_W, map_rect.height)
        self.rect = pygame.Rect(xy, size)
        self.image_x = self.rect.x + 20
        self.image_y = self.rect.y + 20
        self.image_w = 150
        self.font = "consolas"
        self.color = s.RED_DARK
        self.text_h = 20
        self.text_x = self.rect.x + 20
        self.text_y = self.image_y + self.image_w + self.text_h
        self.style = pygame.font.SysFont(self.font, self.text_h)

    def draw(self):
        """ рисует панель в левой части экрана """
        screen = self.game.screen
        character = self.game.get_active_character()
        if not character:
            return
        # фон
        pygame.draw.rect(screen, s.BLACK, self.rect)

        # лицо
        pic = pygame.transform.scale(character.image, (self.image_w, self.image_w))
        screen.blit(pic, (self.image_x, self.image_y))
        if character.item_in_hands:
            pic_ = pygame.transform.scale(character.item_in_hands.image2,
                                          (self.image_w, self.image_w))
            screen.blit(pic_, (self.image_x, self.image_y))

        # текст
        rows1 = [
            "{:<9} {}".format("Name:", character.name),
            "{:<9} {}".format("Health:", character.lives),
            "{:<9} {}".format("Actions:", character.actions),
        ]

        rows2 = list()
        if character.type == "hero":
            # in hands
            in_hands = character.item_in_hands
            if in_hands:
                in_hands = character.item_in_hands.kind
            armor = character.armor
            strength = 0
            if armor:
                armor = character.armor.kind
                strength = character.armor.strength

            # ищет патроны для оружия в рюкзаке героя
            cart_count = 0
            # cart_count_str = ""
            if in_hands:
                for item_i in character.items:
                    # ищет патроны нужного типа в рюкзаке
                    if character.item_in_hands.kind_0 == "gun":  # если в руках оружие
                        # если патроны подходят к оружи.
                        if item_i.kind == character.item_in_hands.cartridge_kind:
                            cart_count = item_i.count
                            # cart_count_str = f"{cart_count}"
                            break

                    # если в руках патроны или гранаты
                    elif character.item_in_hands.kind_0 == "cart":
                        # будет писать кол. патронов которые мы держим
                        cart_count = character.item_in_hands.count
                        break
                    # cart_count_str = cart_count

            # текст
            rows2 = ["{:<9} {}".format("Strength:", strength),
                     "{:<9} {}, {}".format("In hands:", in_hands, cart_count),
                     "{:<9} {}".format("Items in backpack:", len(character.items)),
                     "{:<9} {}, {}".format("Armor:", armor, strength)]

        # рисует текст на дашборде
        rows = rows1 + rows2
        for i, row in enumerate(rows):
            text = self.style.render(row, True, self.color)
            xy = (self.text_x, self.text_y + self.text_h * i)
            screen.blit(text, xy)
