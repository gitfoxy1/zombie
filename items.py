""" Вещи """
import random

from pygame import Surface
from pygame.mixer import Sound

import settings as s
from sprite_on_map import SpriteOnMap

Game = "Game"


class Items(SpriteOnMap):
    """ Вещи """

    def __init__(self, image: str, kind_0: str, kind: str):
        scale = 0.5
        width = int(s.CELL_W * scale)
        size = (width, width)
        super().__init__(image=image, size=size)
        self.kind = kind  # тип вещи: Digle, U.Z.I., Kalashnikov, Mastif, Little Cartridge
        self.kind_0 = kind_0  # тип вещи: gun, cart, steelweapon, armor, medicine, backpack
        sound = s.S_USE.get(kind, s.OH)  # TODO
        self.sound_use = Sound(sound)
        self.sound_breaking = Sound(sound)

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

    def __init__(self, image: str, kind: str):
        super().__init__(image=image, kind_0="gun", kind=kind)
        self.damage = 0  # урон
        self.cartridge_kind = ""  # совместимые патроны
        self.fire_speed = 1  # скорострельность
        self.range = 0  # дальность выстрела
        self.hit_probability = 1  # вероятность попадания


class Digle(Guns):
    """ пистолет Digle """

    def __init__(self):
        super().__init__(image="giftbox.png", kind="Digle")
        self.damage = 2
        self.cartridge_kind = "Little Cartridge"
        self.fire_speed = 1
        self.range = 3
        self.hit_probability = 1


class Uzi(Guns):
    """автомат U.Z.I."""

    def __init__(self):
        super().__init__(image="giftbox.png", kind="U.Z.I.")
        self.damage = 1
        self.cartridge_kind = "Little Cartridge"
        self.fire_speed = 3
        self.range = 3
        self.hit_probability = 0.7


class Kalashnikov(Guns):
    """автомат Kalashnikov"""

    def __init__(self):
        super().__init__(image="giftbox.png", kind="Kalashnikov")
        self.damage = 1
        self.cartridge_kind = "Heavy Cartridge"
        self.fire_speed = 5
        self.range = 3
        self.hit_probability = 0.9


class Mastif(Guns):
    """дробовик Mastif"""

    def __init__(self):
        super().__init__(image="giftbox.png", kind="Mastif")
        self.damage = 4
        self.cartridge_kind = "Fraction"
        self.fire_speed = 1
        self.range = 1
        self.hit_probability = 1


class Mozambyk(Guns):
    """дробовик Mozambyk"""

    def __init__(self):
        super().__init__(image="giftbox.png", kind="Mozambyk")
        self.damage = 3
        self.cartridge_kind = "Fraction"
        self.fire_speed = 1
        self.range = 2
        self.hit_probability = 0.7


class Awp(Guns):
    """снайперская винтовка A.W.P"""

    def __init__(self):
        super().__init__(image="giftbox.png", kind="A.W.P")
        self.damage = 4
        self.cartridge_kind = "Heavy Cartridge"
        self.fire_speed = 1
        self.range = 5
        self.hit_probability = 1


# =====  CARTRIDGE  ==========================================================

class Cartridge(Items):
    """ Класс-родитель для патронов """

    def __init__(self, image: str, kind: str):
        super().__init__(image=image, kind_0="cart", kind=kind)
        self.type = ""
        self.count = 0
        self.count_max = 0


class LittleCartridge(Cartridge):
    """ лёгкие патроны """

    def __init__(self):
        super().__init__(image="giftbox.png", kind="Little Cartridge")
        self.count = 10
        self.count_max = self.count * 3


class HeavyCartridge(Cartridge):
    """ тяжёлые патроны """

    def __init__(self):
        super().__init__(image="giftbox.png", kind="Heavy Cartridge")
        self.count = 10
        self.count_max = self.count * 3


class Fraction(Cartridge):
    """ патроны """

    def __init__(self):
        super().__init__(image="giftbox.png", kind="Fraction")
        self.count = 5
        self.count_max = self.count * 3


# =====  STEEL WEAPON  ==========================================================

class SteelWeapon(Items):
    """ Класс-родитель для холодного оружия """

    def __init__(self, image: str, kind):
        super().__init__(image=image, kind_0="steelweapon", kind=kind)
        self.damage = 0
        self.strength = 0
        self.sound_breaking = Sound(s.S_BREAKING[kind])

    def reduce_strength(self) -> None:
        """ оружие теряет прочность """
        damage = 1 if random.randrange(100) < 50 else 2
        self.strength -= damage


class Knife(SteelWeapon):
    """ ножик """

    def __init__(self):
        super().__init__(image="giftbox.png", kind="Knife")
        self.damage = 3
        self.strength = 5


class Bat(SteelWeapon):
    """ Bat """

    def __init__(self):
        super().__init__(image="giftbox.png", kind="Bat")
        self.damage = 2
        self.strength = 10


# =====  ARMOR  ==========================================================

class Armor(Items):
    """ Класс-родитель для брони """

    def __init__(self, image: str, kind: str):
        super().__init__(image=image, kind_0="armor", kind=kind)
        self.strength = 0  # стойкость брони


class Armor1(Armor):
    """ броня """

    def __init__(self):
        super().__init__(image="giftbox.png", kind="Armor level 1")
        self.strength = 2


class Armor2(Armor):
    """ броня """

    def __init__(self):
        super().__init__(image="giftbox.png", kind="armor_level_2")
        self.strength = 3


class Armor3(Armor):
    """ броня """

    def __init__(self):
        super().__init__(image="giftbox.png", kind="armor_level_3")
        self.strength = 4


# =====  BACKPACK_  ==========================================================

class Backpack0(Items):
    """ Класс-родитель для рюкзак """

    def __init__(self, image: str, kind: str):
        super().__init__(image=image, kind_0="backpack", kind=kind)
        self.capacity = 0  # дополнительная вместимость рюкзака


class Backpack1(Backpack0):
    """ рюкзак """

    def __init__(self):
        super().__init__(image="giftbox.png", kind="backpack_level_1")
        self.capacity = 1


class Backpack2(Backpack0):
    """ рюкзак """

    def __init__(self):
        super().__init__(image="giftbox.png", kind="backpack_level_2")
        self.capacity = 2


class Backpack3(Backpack0):
    """ рюкзак """

    def __init__(self):
        super().__init__(image="giftbox.png", kind="backpack_level_3")
        self.capacity = 3


# =====  MEDICINE  ==========================================================

class Medicine(Items):
    """ Класс-родитель для лекарств """

    def __init__(self, image: str, kind: str):
        super().__init__(image=image, kind_0="medicine", kind=kind)
        self.heal = 0
        self.heal_target = ""


class Medikit(Medicine):
    """ лекарство """

    def __init__(self):
        super().__init__(image="giftbox.png", kind="Medikit")
        self.heal = 5
        self.heal_target = "health"


class Cotton(Medicine):
    """ нитки """

    def __init__(self):
        super().__init__(image="giftbox.png", kind="Cotton")
        self.heal = 1
        self.heal_target = "armor"


# =====  FUNCTIONS  ==========================================================

def items_generator(count: int) -> list:
    """ рандомно создаёт вещи. Обязательные, одно оружие, патроны, ... остальное random  """
    items = list()

    # вещи которые должны быть на карте обязательно
    items_mandatory = [
        # random.choice([Digle, Uzi]), LittleCartridge,  # Little Gun
        # random.choice([Kalashnikov, Awp]), HeavyCartridge,  # Heavy Gun
        # random.choice([Mozambyk, Mastif]), Fraction,  # Fraction Gun
        # random.choice([Knife, Bat]),  # Steel Weapon
        # random.choice([Armor1, Armor2, Armor3]),  # Armor
        # random.choice([Backpack1, Backpack2, Backpack3]),  # Backpack
        # random.choice([Medikit, Cotton])  # Medicine
    ]
    for item in items_mandatory:
        items.append(item())

    # дополнительные вещи
    while len(items) < count:
        items_extra = [
            # [Digle for _ in range(random.randrange(1, 3))],
            # [Uzi for _ in range(random.randrange(1, 3))],
            # [LittleCartridge for _ in range(random.randrange(1, 3))],
            # [Bat for _ in range(random.randrange(1, 3))],
            [Knife for _ in range(random.randrange(1, 3))],
        ]
        items_extra = [i for l in items_extra for i in l]
        item_extra = random.choice(items_extra)
        items.append(item_extra())
    return items
