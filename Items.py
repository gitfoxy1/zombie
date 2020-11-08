import os
from typing import Optional

import pygame
from pygame import Surface

import constants as c


class Items:
    """ Вещи """
    kind: Optional[str]  # тип вещи: Digle, U.Z.I., Kalashnikov, Mastif, Little Cartridge
    kind_0: Optional[str]  # тип вещи: gun, cart, steelweapon, armor, medicines, backpack
    image_on_map: str  # картинка на карте

    def __init__(self):
        self.kind = None
        self.kind_0 = None
        self.image = None  # todo
        self.image_on_map = "?"  # todo

    # noinspection PyUnresolvedReferences
    def draw(self, screen: Surface, cell: "Cell"):
        """ Рисует персонажа на карте """
        cell_x = c.CELL_W * cell.xy[0]  # координаты клетки на экрана
        cell_y = c.CELL_W * cell.xy[1]
        font = pygame.font.SysFont("Times", 100)
        text = font.render(self.image_on_map, True, c.RED)
        rect = text.get_rect()
        rect.centerx = cell_x + c.CELL_W // 2
        rect.centery = cell_y + c.CELL_W // 2
        screen.blit(text, (rect.x, rect.y))
        # pygame.draw.rect(screen, c.BLUE, rect, 1)  # test


class Guns(Items):
    """ Класс-родитель для оружия """

    def __init__(self):
        super().__init__()
        self.damage = None
        self.cartridge_kind = None
        self.fire_speed = None
        self.range = None
        self.kind_0 = "gun"
        self.sound_shot = None


class Digle(Guns):
    """Характеристика пистолета"""

    def __init__(self):
        super().__init__()
        self.kind = "Digle"
        self.damage = 2
        self.cartridge_kind = "Little Cartridge"
        self.fire_speed = 1
        self.range = 3
        self.sound_shot = pygame.mixer.Sound(os.path.join(c.SOUNDS_DIR, "gun_digle.wav"))


class Uzi(Guns):
    def __init__(self):
        super().__init__()
        self.kind = "U.Z.I."
        self.damage = 1
        self.cartridge_kind = "Little Cartridge"
        self.fire_speed = 3
        self.range = 3
        self.sound_shot = pygame.mixer.Sound(os.path.join(c.SOUNDS_DIR, "gun_U_Z_I.wav"))


class Kalashnikov(Guns):
    def __init__(self):
        super().__init__()
        self.kind = "Kalashnikov"
        self.damage = 1
        self.cartridge_kind = "Heavy Cartridge"
        self.fire_speed = 5
        self.range = 3
        self.sound_shot = pygame.mixer.Sound(os.path.join(c.SOUNDS_DIR, "01_gun kalashnikov1.wav"))


class Mastif(Guns):
    def __init__(self):
        super().__init__()
        self.kind = "Mastif"
        self.damage = 3
        self.cartridge_kind = "Fraction"
        self.fire_speed = 1
        self.range = 2
        self.sound_shot = pygame.mixer.Sound(os.path.join(c.SOUNDS_DIR, "gun_Mastif.wav"))


class Mozambyk(Guns):
    def __init__(self):
        super().__init__()
        self.kind = "Mozambyk"
        self.damage = 2
        self.cartridge_kind = "Fraction"
        self.fire_speed = 1
        self.range = 2
        self.sound_shot = pygame.mixer.Sound(os.path.join(c.SOUNDS_DIR, "gun_mazombyk.wav"))


class Awp(Guns):
    def __init__(self):
        super().__init__()
        self.kind = "A.W.P"
        self.damage = 3
        self.cartridge_kind = "Heavy Cartridge"
        self.fire_speed = 1
        self.range = 4
        self.sound_shot = pygame.mixer.Sound(os.path.join(c.SOUNDS_DIR, "gun_A.W.P.wav"))


class Cartridge(Items):
    """ патроны """

    def __init__(self):
        super().__init__()
        self.type = None
        self.count = None
        self.kind_0 = "cart"


class LittleCartridge(Cartridge):
    def __init__(self):
        super().__init__()
        self.kind = "Little Cartridge"
        self.count = 20
        self.count_max = self.count * 3


class HeavyCartridge(Cartridge):
    def __init__(self):
        super().__init__()
        self.kind = "Heavy Cartridge"
        self.count = 10
        self.count_max = self.count * 3


class Fraction(Cartridge):
    def __init__(self):
        super().__init__()
        self.kind = "Fraction"
        self.count = 8
        self.count_max = self.count * 3


class SteelWeapon(Items):
    """ Класс-родитель для оружия """

    def __init__(self):
        super().__init__()
        self.damage = None
        self.kind_0 = "steelweapon"


class Knife(SteelWeapon):
    def __init__(self):
        super().__init__()
        self.kind = "Knife"
        self.damage = 3
        self.strength = 5


class Bat(SteelWeapon):
    def __init__(self):
        super().__init__()
        self.kind = "Bat"
        self.damage = 2
        self.strength = 10


class Armor(Items):
    """ броня """
    strength: int = 0  # стойкость брони

    def __init__(self):
        super().__init__()
        self.kind_0 = "armor"
        self.strength = 0


class Armor_level_1(Armor):  # todo armor
    def __init__(self):
        super().__init__()
        self.kind = "Armor level 1"
        self.strength = 2


class Armor_level_2(Armor):
    def __init__(self):
        super().__init__()
        self.kind = "armor_level_2"
        self.strength = 3


class Armor_level_3(Armor):
    def __init__(self):
        super().__init__()
        self.kind = "armor_level_3"
        self.strength = 4


class Backpack_(Items):
    capacity: int = 0  # вместимость рюкзака

    def __init__(self):
        super().__init__()
        self.kind_0 = "backpack"
        self.capacity = 0


class Backpack_level_1(Backpack_):  # todo Backpack
    def __init__(self):
        super().__init__()
        self.kind = "backpack_level_1"
        self.capacity = 1


class Backpack_level_2(Backpack_):
    def __init__(self):
        super().__init__()
        self.kind = "backpack_level_2"
        self.capacity = 2


class Backpack_level_3(Backpack_):
    def __init__(self):
        super().__init__()
        self.kind = "backpack_level_3"
        self.capacity = 3


class Medicines(Items):
    def __init__(self):
        super().__init__()
        self.heal = None
        self.heal_target = None
        self.kind_0 = "medicines"


class Medikit(Medicines):
    def __init__(self):
        super().__init__()
        self.heal = 3
        self.heal_target = "health"
        self.kind_0 = "medicines"
        self.kind = "Medikit"


class Cotton(Medicines):
    """ нитки """
    def __init__(self):
        super().__init__()
        self.heal = 1
        self.heal_target = "armor"
        self.kind_0 = "medicines"
        self.kind = "cotton"
