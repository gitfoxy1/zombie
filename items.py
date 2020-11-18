""" Вещи """
import os
import random

import pygame
from pygame import Surface

import settings as s
from sprite_on_map import SpriteOnMap

Game = "Game"


class Items(SpriteOnMap):
    """ Вещи """

    def __init__(self, image: str):
        scale = 0.5
        width = int(s.CELL_W * scale)
        size = (width, width)
        super().__init__(image=image, size=size)

        # тип вещи: Digle, U.Z.I., Kalashnikov, Mastif, Little Cartridge
        self.kind: str = ""
        # тип вещи: gun, cart, steelweapon, armor, medicine, backpack
        self.kind_0: str = ""

    # noinspection PyUnresolvedReferences
    def draw(self, screen: Surface, cell: "Cell"):
        """ Рисует персонажа на карте """

        cell_x = s.CELL_W * cell.xy[0]  # координаты клетки на экрана
        cell_y = s.CELL_W * cell.xy[1]
        # font = pygame.font.SysFont("Times", 75)
        # text = font.render(self.image, True, s.BLACK)
        rect = self.get_rect()
        rect.centerx = cell_x + s.CELL_W // 2
        rect.centery = cell_y + s.CELL_W // 2
        screen.blit(self.image, (rect.x, rect.y))
        # pygame.draw.rect(screen, s.BLUE, rect, 1)  # test


# =====  GUNS  ==========================================================

class Guns(Items):
    """ Класс-родитель для оружия """

    def __init__(self, image: str):
        super().__init__(image)
        self.damage = None
        self.cartridge_kind = None
        self.fire_speed = None
        self.range = None
        self.kind_0 = "gun"
        self.sound_shot = None


class Digle(Guns):
    """ пистолет Digle """

    def __init__(self):
        image = "giftbox.png"
        super().__init__(image)
        self.kind = "Digle"
        self.damage = 2
        self.cartridge_kind = "Little Cartridge"
        self.fire_speed = 1
        self.range = 3
        self.sound_shot = pygame.mixer.Sound(os.path.join(s.SOUNDS_DIR, "gun_digle.wav"))


class Uzi(Guns):
    """автомат U.Z.I."""

    def __init__(self):
        image = "giftbox.png"
        super().__init__(image)
        self.kind = "U.Z.I."
        self.damage = 1
        self.cartridge_kind = "Little Cartridge"
        self.fire_speed = 3
        self.range = 3
        self.sound_shot = pygame.mixer.Sound(os.path.join(s.SOUNDS_DIR, "gun_U_Z_I.wav"))


class Kalashnikov(Guns):
    """автомат Kalashnikov"""

    def __init__(self):
        image = "giftbox.png"
        super().__init__(image)
        self.kind = "Kalashnikov"
        self.damage = 1
        self.cartridge_kind = "Heavy Cartridge"
        self.fire_speed = 5
        self.range = 3
        self.sound_shot = pygame.mixer.Sound(os.path.join(s.SOUNDS_DIR, "01_gun kalashnikov1.wav"))


class Mastif(Guns):
    """Mastif"""

    def __init__(self):
        image = "giftbox.png"
        super().__init__(image)
        self.kind = "Mastif"
        self.damage = 3
        self.cartridge_kind = "Fraction"
        self.fire_speed = 1
        self.range = 2
        self.sound_shot = pygame.mixer.Sound(os.path.join(s.SOUNDS_DIR, "gun_Mastif.wav"))


class Mozambyk(Guns):
    """Mozambyk"""

    def __init__(self):
        image = "giftbox.png"
        super().__init__(image)
        self.kind = "Mozambyk"
        self.damage = 2
        self.cartridge_kind = "Fraction"
        self.fire_speed = 1
        self.range = 2
        self.sound_shot = pygame.mixer.Sound(os.path.join(s.SOUNDS_DIR, "gun_mazombyk.wav"))


class Awp(Guns):
    """A.W.P"""

    def __init__(self):
        image = "giftbox.png"
        super().__init__(image)
        self.kind = "A.W.P"
        self.damage = 3
        self.cartridge_kind = "Heavy Cartridge"
        self.fire_speed = 1
        self.range = 4
        self.sound_shot = pygame.mixer.Sound(os.path.join(s.SOUNDS_DIR, "gun_A.W.P.wav"))


# =====  CARTRIDGE  ==========================================================

class Cartridge(Items):
    """ Класс-родитель для патронов """

    def __init__(self, image: str):
        super().__init__(image)
        self.type = None
        self.count = None
        self.kind_0 = "cart"


class LittleCartridge(Cartridge):
    """ лёгкие патроны """

    def __init__(self):
        image = "giftbox.png"
        super().__init__(image)
        self.kind = "Little Cartridge"
        self.count = 20
        self.count_max = self.count * 3


class HeavyCartridge(Cartridge):
    """ тяжёлые патроны """

    def __init__(self):
        image = "giftbox.png"
        super().__init__(image)
        self.kind = "Heavy Cartridge"
        self.count = 10
        self.count_max = self.count * 3


class Fraction(Cartridge):
    """ патроны """

    def __init__(self):
        image = "giftbox.png"
        super().__init__(image)
        self.kind = "Fraction"
        self.count = 8
        self.count_max = self.count * 3


# =====  STEEL WEAPON  ==========================================================

class SteelWeapon(Items):
    """ Класс-родитель для оружия """

    def __init__(self, image: str):
        super().__init__(image)
        self.damage = None
        self.kind_0 = "steelweapon"


class Knife(SteelWeapon):
    """ ножик """

    def __init__(self):
        image = "giftbox.png"
        super().__init__(image)
        self.kind = "Knife"
        self.damage = 3
        self.strength = 5


class Bat(SteelWeapon):
    """ Bat """

    def __init__(self):
        image = "giftbox.png"
        super().__init__(image)
        self.kind = "Bat"
        self.damage = 2
        self.strength = 10


# =====  ARMOR  ==========================================================

class Armor(Items):
    """ Класс-родитель для брони """

    def __init__(self, image: str):
        super().__init__(image)
        self.kind_0 = "armor"
        self.strength = 0  # стойкость брони


class Armor1(Armor):
    """ броня """

    def __init__(self):
        image = "giftbox.png"
        super().__init__(image)
        self.kind = "Armor level 1"
        self.strength = 2


class Armor2(Armor):
    """ броня """

    def __init__(self):
        image = "giftbox.png"
        super().__init__(image)
        self.kind = "armor_level_2"
        self.strength = 3


class Armor3(Armor):
    """ броня """

    def __init__(self):
        image = "giftbox.png"
        super().__init__(image)
        self.kind = "armor_level_3"
        self.strength = 4


# =====  BACKPACK_  ==========================================================

class Backpack0(Items):
    """ Класс-родитель для рюкзак """

    def __init__(self, image: str):
        super().__init__(image)
        self.kind_0 = "backpack"
        self.capacity = 0  # вместимость рюкзака


class Backpack1(Backpack0):
    """ рюкзак """

    def __init__(self):
        image = "giftbox.png"
        super().__init__(image)
        self.kind = "backpack_level_1"
        self.capacity = 1


class Backpack2(Backpack0):
    """ рюкзак """

    def __init__(self):
        image = "giftbox.png"
        super().__init__(image)
        self.kind = "backpack_level_2"
        self.capacity = 2


class Backpack3(Backpack0):
    """ рюкзак """

    def __init__(self):
        image = "giftbox.png"
        super().__init__(image)
        self.kind = "backpack_level_3"
        self.capacity = 3


# =====  MEDICINE  ==========================================================

class Medicine(Items):
    """ Класс-родитель для лекарств """

    def __init__(self, image: str):
        super().__init__(image)
        self.heal = None
        self.heal_target = None
        self.kind_0 = "medicine"


class Medikit(Medicine):
    """ лекарство """

    def __init__(self):
        image = "giftbox.png"
        super().__init__(image)
        self.heal = 3
        self.heal_target = "health"
        self.kind_0 = "medicine"
        self.kind = "Medikit"


class Cotton(Medicine):
    """ нитки """

    def __init__(self):
        image = "giftbox.png"
        super().__init__(image)
        self.heal = 1
        self.heal_target = "armor"
        self.kind_0 = "medicine"
        self.kind = "Cotton"


# =====  FUNCTIONS  ==========================================================

def items_generator(count: int) -> list:
    """ рандомно создаёт вещи. Обязательные, одно оружие, патроны, ... остальное random  """
    items = list()

    # вещи которые должны быть на карте обязательно
    items_mandatory = [
        random.choice([Digle, Uzi]), LittleCartridge,  # Little Gun
        random.choice([Kalashnikov, Awp]), HeavyCartridge,  # Heavy Gun
        random.choice([Mozambyk, Mastif]), Fraction,  # Fraction Gun
        random.choice([Knife, Bat]),  # Steel Weapon
        random.choice([Armor1, Armor2, Armor3]),  # Armor
        random.choice([Backpack1, Backpack2, Backpack3]),  # Backpack
        random.choice([Medikit, Cotton])  # Medicine
    ]
    for item in items_mandatory:
        items.append(item())

    # дополнительные вещи
    while len(items) < count:
        items_extra = [
            [Digle for _ in range(random.randrange(1, 3))],
            [Uzi for _ in range(random.randrange(1, 3))],
            [LittleCartridge for _ in range(random.randrange(1, 3))],
        ]
        items_extra = [i for l in items_extra for i in l]
        item_extra = random.choice(items_extra)
        items.append(item_extra())
    return items
