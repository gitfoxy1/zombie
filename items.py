""" Вещи """
import os
import random

import pygame
from pygame import Surface
from pygame.mixer import Sound

import settings as s
from sprite_on_map import SpriteOnMap

Game = "Game"


class Items(SpriteOnMap):
    """ Вещи """

    def __init__(self, image: str, image2: str, kind_0: str, kind: str, game: Game):
        size = (90, 90)
        super().__init__(image=image, size=size, game=game)
        image2: Surface = pygame.image.load(os.path.join(s.IMAGES_DIR, image2))
        self.image2: Surface = pygame.transform.scale(image2, size)
        self.kind_0 = kind_0  # тип вещи: gun, cart, steelweapon, armor, medicine, backpack
        self.kind = kind  # тип вещи: Digle, U.Z.I., Kalashnikov, Mastif, Little Cartridge
        sound = s.S_USE.get(kind, s.OH)
        self.sound_use = Sound(sound)
        self.sound_breaking = Sound(sound)


# =====  GUNS  ==========================================================

class Guns(Items):
    """ Класс-родитель для оружия """

    def __init__(self, image: str, image2: str, kind: str, game: Game):
        super().__init__(image=image, image2=image2, kind_0="gun", kind=kind, game=game)
        self.damage = 0  # урон
        self.cartridge_kind = ""  # совместимые патроны
        self.fire_speed = 1  # скорострельность
        self.range = 0  # дальность выстрела
        self.hit_probability = 1  # вероятность попадания


class Digle(Guns):
    """ пистолет Digle """

    def __init__(self, game: Game):
        super().__init__(image="digle.png", image2="digle_in_hands.png", kind="Digle", game=game)
        self.damage = 2
        self.cartridge_kind = "Little Cartridge"
        self.fire_speed = 1
        self.range = 3
        self.hit_probability = 0.8


class Uzi(Guns):
    """пистолет пулимёт U.Z.I."""

    def __init__(self, game: Game):
        super().__init__(image="U.Z.I.png", image2="U.Z.I_in_hands.png", kind="U.Z.I.", game=game)
        self.damage = 1
        self.cartridge_kind = "Little Cartridge"
        self.fire_speed = 3
        self.range = 3
        self.hit_probability = 0.6


class Kalashnikov(Guns):
    """автомат Kalashnikov"""

    def __init__(self, game: Game):
        super().__init__(image="kalashnikov.png", image2="kalashnikov_in_hands.png",
                         kind="Kalashnikov", game=game)
        self.damage = 1
        self.cartridge_kind = "Heavy Cartridge"
        self.fire_speed = 5
        self.range = 3
        self.hit_probability = 0.7


class Mastif(Guns):
    """дробовик Mastif"""

    def __init__(self, game: Game):
        super().__init__(image="mastif.png", image2="mastif_in_hands.png", kind="Mastif", game=game)
        self.damage = 4
        self.cartridge_kind = "Fraction"
        self.fire_speed = 1
        self.range = 1
        self.hit_probability = 0.8


class Mozambyk(Guns):
    """дробовик Mozambyk"""

    def __init__(self, game: Game):
        super().__init__(image="mozambyk.png", image2="mozambyk_in_hands.png", kind="Mozambyk",
                         game=game)
        self.damage = 3
        self.cartridge_kind = "Fraction"
        self.fire_speed = 1
        self.range = 2
        self.hit_probability = 0.7


class Awp(Guns):
    """снайперская винтовка A.W.P"""

    def __init__(self, game: Game):
        super().__init__(image="awp.png", image2="awp_in_hands.png", kind="A.W.P", game=game)
        self.damage = 4
        self.cartridge_kind = "Heavy Cartridge"
        self.fire_speed = 1
        self.range = 5
        self.hit_probability = 0.8


# =====  CARTRIDGE  ==========================================================


class Cartridge(Items):
    """ Класс-родитель для патронов """

    def __init__(self, image: str, image2: str, kind: str, game: Game):
        super().__init__(image=image, image2=image2, kind_0="cart", kind=kind, game=game)
        self.type = ""
        self.count = 0
        self.count_max = 0

    @classmethod
    def little(cls, game: Game):
        """ лёгкие патроны  """
        cartridge = cls(image="little.png", image2="little_in_hands.png", kind="Little Cartridge",
                        game=game)
        cartridge.count_max = 40
        cartridge.count = 10
        cartridge.image_in_hands = "little.png"
        return cartridge


class HeavyCartridge(Cartridge):
    """ тяжёлые патроны """

    def __init__(self, game: Game):
        super().__init__(image="heavy.png", image2="heavy_in_hands.png", kind="Heavy Cartridge",
                         game=game)
        self.count = 10
        self.count_max = self.count * 4


class Fraction(Cartridge):
    """ патроны """

    def __init__(self, game: Game):
        super().__init__(image="fraction.png", image2="fraction_in_hands.png", kind="Fraction",
                         game=game)
        self.count = 5
        self.count_max = self.count * 4


# =====  STEEL WEAPON  ==========================================================

class SteelWeapon(Items):
    """ Класс-родитель для холодного оружия """

    def __init__(self, image: str, image2: str, kind: str, game: Game):
        super().__init__(image=image, kind_0="steelweapon", image2=image2, kind=kind, game=game)
        self.damage = 0
        self.strength = 0
        self.sound_breaking = Sound(s.S_BREAKING[kind])

    def reduce_strength(self) -> None:
        """ оружие теряет прочность """
        damage = 1 if random.randrange(100) < 50 else 2
        self.strength -= damage


class Knife(SteelWeapon):
    """ ножик """

    def __init__(self, game: Game):
        super().__init__(image="knife.png", image2="knife_in_hands.png", kind="Knife", game=game)
        self.damage = 3
        self.strength = 5


class Bat(SteelWeapon):
    """ Bat """

    def __init__(self, game: Game):
        super().__init__(image="bat_.png", image2="bat_in_hands.png", kind="Bat", game=game)
        self.damage = 2
        self.strength = 10


# =====  ARMOR  ==========================================================

class Armor(Items):
    """ Класс-родитель для брони """

    def __init__(self, image: str, image2: str, kind: str, game: Game):
        super().__init__(image=image, kind_0="armor", image2=image2, kind=kind, game=game)
        self.strength = 0  # стойкость брони

    @classmethod
    def lvl1(cls, game: Game):
        """ броня уровень 1 """
        armor = cls(image="armor_1.png", image2="armor_1_in_hands.png", kind="armor_level_1",
                    game=game)
        armor.strength = 2
        return armor

    @classmethod
    def lvl2(cls, game: Game):
        """ броня уровень 1 """
        armor = cls(image="armor_2.png", image2="armor_2_in_hands.png", kind="armor_level_2",
                    game=game)
        armor.strength = 3
        return armor

    @classmethod
    def lvl3(cls, game: Game):
        """ броня уровень 1 """
        armor = cls(image="armor_3.png", image2="armor_3_in_hands.png", kind="armor_level_3",
                    game=game)
        armor.strength = 4
        return armor


# =====  BACKPACK_  ==========================================================

class Backpack0(Items):
    """ вещь рюкзак """

    def __init__(self, image: str, image2: str, kind: str, game: Game):
        super().__init__(image=image, image2=image2, kind=kind, kind_0="backpack", game=game)
        self.capacity = 0  # дополнительная вместимость рюкзака

    @classmethod
    def lvl1(cls, game: Game):
        """ рюкзак, дополнительная вместимость 1 слот """
        image = "backpack_1.png"
        image2 = "backpack_1_in_hands.png"
        kind = "backpack1"
        backpack = cls(image, image2, kind, game)
        backpack.capacity = 1
        return backpack

    @classmethod
    def lvl2(cls, game: Game):
        """ рюкзак, дополнительная вместимость 2 слота """
        image = "backpack_2.png"
        image2 = "backpack_2_in_hands.png"
        kind = "backpack2"
        backpack = cls(image, image2, kind, game)
        backpack.capacity = 2
        return backpack

    @classmethod
    def lvl3(cls, game: Game):
        """ рюкзак, дополнительная вместимость 3 слота """
        image = "backpack_3.png"
        image2 = "bacpack_3_in_hands.png"
        kind = "backpack3"
        backpack = cls(image, image2, kind, game)
        backpack.capacity = 3
        return backpack


# =====  MEDICINE  ==========================================================

class Medicine(Items):
    """ Класс-родитель для лекарств """

    def __init__(self, image: str, image2: str, kind: str, game: Game):
        super().__init__(image=image, image2=image2, kind_0="medicine", kind=kind, game=game)
        self.heal = 0
        self.heal_target = ""

    @classmethod
    def medikit(cls, game: Game):
        """ лекарство """
        medikit = cls(image="medikit.png", image2="medikit_in_hands.png", kind="Medikit", game=game)
        medikit.heal = 5
        medikit.heal_target = "health"
        medikit.image_in_hands = "medikit.png"
        return medikit

    @classmethod
    def cotton(cls, game: Game):
        """ нитки """
        medikit = cls(image="coath.png", image2="coath_in_hands.png", kind="Cotton", game=game)
        medikit.heal = 1
        medikit.heal_target = "armor"
        medikit.image_in_hands = "coath.png"
        return medikit


# =====  FUNCTIONS  ==========================================================

def items_generator(count: int, game: Game) -> list:
    """ рандомно создаёт вещи. Обязательные, одно оружие, патроны, ... остальное random  """
    items = list()

    # вещи которые должны быть на карте обязательно
    items_mandatory = [
        random.choice([Backpack0.lvl1]),  # Backpack
        random.choice([Digle, Uzi]), Cartridge.little,  # Little Gun
        random.choice([Kalashnikov, Awp]), HeavyCartridge,  # Heavy Gun
        random.choice([Mozambyk, Mastif]), Fraction,  # Fraction Gun
        random.choice([Knife, Bat]),  # Steel Weapon
        random.choice([Armor.lvl1, Armor.lvl2, Armor.lvl3]),  # Armor
        random.choice([Backpack0.lvl1, Backpack0.lvl2, Backpack0.lvl3]),  # Backpack
        random.choice([Medicine.medikit, Medicine.cotton]),  # Medicine
        # random.choice([Digle, Uzi, Kalashnikov, Awp, Mozambyk, Mastif, Knife, Bat]),
        # random.choice([Armor1, Armor2]),  # Armor
        # random.choice([Uzi, Kalashnikov, Mozambyk, Bat]),
        # random.choice([Backpack1, Backpack2]),  # Backpack
        # random.choice([Uzi, Bat]),
        # random.choice([Backpack1, Armor1]),  # Backpack
    ]
    for item_mandatory in items_mandatory:
        item = item_mandatory(game=game)
        items.append(item)

    # дополнительные вещи
    while len(items) < count:
        items_extra = [
            [HeavyCartridge for _ in range(random.randrange(1, 2))],
            [Cartridge.little for _ in range(random.randrange(1, 2))],
            [Fraction for _ in range(random.randrange(1, 2))],
            [Medicine.medikit for _ in range(random.randrange(1, 3))],
            [Medicine.cotton for _ in range(random.randrange(1, 3))],
        ]
        items_extra = [i for i_l in items_extra for i in i_l]
        item_extra = random.choice(items_extra)
        item = item_extra(game=game)
        items.append(item)
    return items
