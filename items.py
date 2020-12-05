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
        scale = 0.5
        width = int(s.CELL_W * scale)
        size = (90, 90)
        super().__init__(image=image, size=size, game=game)

        image2: Surface = pygame.image.load(os.path.join(s.IMAGES_DIR, image2))
        self.image2: Surface = pygame.transform.scale(image2, size)

        self.kind = kind  # тип вещи: Digle, U.Z.I., Kalashnikov, Mastif, Little Cartridge
        self.kind_0 = kind_0  # тип вещи: gun, cart, steelweapon, armor, medicine, backpack
        sound = s.S_USE.get(kind, s.OH)  # todo sounds
        self.sound_use = Sound(sound)
        self.sound_breaking = Sound(sound)

    # # noinspection PyUnresolvedReferences
    # def draw(self, screen: Surface, cell: "Cell"):
    #     """ Рисует персонажа на карте """
    #
    #     cell_x = s.CELL_W * cell.xy[0]  # координаты клетки на экрана
    #     cell_y = s.CELL_W * cell.xy[1]
    #     # font = pygame.font.SysFont("Times", 75)
    #     # text = font.render(self.image, True, s.BLACK)
    #     rect = self.get_rect()
    #     rect.centerx = cell_x + s.CELL_W // 2
    #     rect.centery = cell_y + s.CELL_W // 2
    #     screen.blit(self.image, (rect.x, rect.y))
    #     # pygame.draw.rect(screen, s.BLUE, rect, 1)  # test


# =====  GUNS  ==========================================================

class Guns(Items):
    """ Класс-родитель для оружия """

    def __init__(self, image: str, image2: str, kind: str, game: Game):
        super().__init__(image=image,  image2=image2, kind_0="gun", kind=kind, game=game)
        self.damage = 0  # урон
        self.cartridge_kind = ""  # совместимые патроны
        self.fire_speed = 1  # скорострельность
        self.range = 0  # дальность выстрела
        self.hit_probability = 1  # вероятность попадания


class Digle(Guns):
    """ пистолет Digle """

    def __init__(self, game: Game):
        super().__init__(image="giftbox.png", image2="deagle_in_hands.png", kind="Digle", game=game)
        self.damage = 2
        self.cartridge_kind = "Little Cartridge"
        self.fire_speed = 1
        self.range = 3
        self.hit_probability = 0.8
        self.image_in_hands = "deagle.png"


class Uzi(Guns):
    """пистолет пулимёт U.Z.I."""

    def __init__(self, game: Game):
        super().__init__(image="U.Z.I.png", image2="U.Z.I_in_hands.png", kind="U.Z.I.", game=game)
        self.damage = 1
        self.cartridge_kind = "Little Cartridge"
        self.fire_speed = 3
        self.range = 3
        self.hit_probability = 0.6
        self.image_in_hands = "U.Z.I_in_hands.png"


class Kalashnikov(Guns):
    """автомат Kalashnikov"""

    def __init__(self, game: Game):
        super().__init__(image="kalashnikov.png",image2="kalashnikov_in_hands.png", kind="Kalashnikov", game=game)
        self.damage = 1
        self.cartridge_kind = "Heavy Cartridge"
        self.fire_speed = 5
        self.range = 3
        self.hit_probability = 0.7
        self.image_in_hands = "kalashnikov.png"


class Mastif(Guns):
    """дробовик Mastif"""

    def __init__(self, game: Game):
        super().__init__(image="mastif.png", image2="mastif_in_hands.png", kind="Mastif", game=game)
        self.damage = 4
        self.cartridge_kind = "Fraction"
        self.fire_speed = 1
        self.range = 1
        self.hit_probability = 0.8
        self.image_in_hands = "mastif.png"


class Mozambyk(Guns):
    """дробовик Mozambyk"""

    def __init__(self, game: Game):
        super().__init__(image="mozambyk.png", image2="mozambyk_in_hands.png", kind="Mozambyk", game=game)
        self.damage = 3
        self.cartridge_kind = "Fraction"
        self.fire_speed = 1
        self.range = 2
        self.hit_probability = 0.7
        self.image_in_hands = "mozambyk.png"


class Awp(Guns):
    """снайперская винтовка A.W.P"""

    def __init__(self, game: Game):
        super().__init__(image="awp.png", image2="awp_in_hands.png", kind="A.W.P", game=game)
        self.damage = 3
        self.cartridge_kind = "Heavy Cartridge"
        self.fire_speed = 1
        self.range = 5
        self.hit_probability = 0.8
        self.image_in_hands = "awp.png"

# =====  CARTRIDGE  ==========================================================

class Cartridge(Items):
    """ Класс-родитель для патронов """

    def __init__(self, image: str, image2: str, kind: str, game: Game):
        super().__init__(image=image, image2=image2, kind_0="cart", kind=kind, game=game)
        self.type = ""
        self.count = 0
        self.count_max = 0


class LittleCartridge(Cartridge):
    """ лёгкие патроны """

    def __init__(self, game: Game):
        super().__init__(image="little.png", image2="awp_in_hands.png", kind="Little Cartridge", game=game)
        self.count = 10
        self.count_max = self.count * 4
        self.image_in_hands = "little.png"


class HeavyCartridge(Cartridge):
    """ тяжёлые патроны """

    def __init__(self, game: Game):
        super().__init__(image="heavy.png", image2="awp_in_hands.png", kind="Heavy Cartridge", game=game)
        self.count = 10
        self.count_max = self.count * 4
        self.image_in_hands = "heavy.png"


class Fraction(Cartridge):
    """ патроны """

    def __init__(self, game: Game):
        super().__init__(image="fraction.png", image2="awp_in_hands.png", kind="Fraction", game=game)
        self.count = 5
        self.count_max = self.count * 4
        self.image_in_hands = "fraction.png"


# =====  STEEL WEAPON  ==========================================================

class SteelWeapon(Items):
    """ Класс-родитель для холодного оружия """

    def __init__(self, image: str, kind, game: Game):
        super().__init__(image=image, kind_0="steelweapon", image2="U.Z.I_in_hands.png", kind=kind, game=game)
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
        super().__init__(image="knife.png", image2="awp_in_hands.png", kind="Knife", game=game)
        self.damage = 3
        self.strength = 5
        self.image_in_hands = "knife.png"


class Bat(SteelWeapon):
    """ Bat """

    def __init__(self, game: Game):
        super().__init__(image="bat_.png", kind="Bat", game=game)
        self.damage = 2
        self.strength = 10
        self.image_in_hands = "bat_.png"



# =====  ARMOR  ==========================================================

class Armor(Items):
    """ Класс-родитель для брони """

    def __init__(self, image: str, kind: str, game: Game):
        super().__init__(image=image, kind_0="armor",image2="U.Z.I_in_hands.png", kind=kind, game=game)
        self.strength = 0  # стойкость брони


class Armor1(Armor):
    """ броня """

    def __init__(self, game: Game):
        super().__init__(image="armor_1.png", kind="Armor level 1", game=game)
        self.strength = 2
        self.image_in_hands = "armor_1.png"



class Armor2(Armor):
    """ броня """

    def __init__(self, game: Game):
        super().__init__(image="armor_2.png", kind="armor_level_2", game=game)
        self.strength = 3
        self.image_in_hands = "armor_2.png"



class Armor3(Armor):
    """ броня """

    def __init__(self, game: Game):
        super().__init__(image="armor_3.png", kind="armor_level_3", game=game)
        self.strength = 4
        self.image_in_hands = "armor_3.png"



# =====  BACKPACK_  ==========================================================

class Backpack0(Items):
    """ Класс-родитель для рюкзак """

    def __init__(self, image: str, kind: str, game: Game):
        super().__init__(image=image, kind_0="backpack",image2="U.Z.I_in_hands.png", kind=kind, game=game)
        self.capacity = 0  # дополнительная вместимость рюкзака


class Backpack1(Backpack0):
    """ рюкзак """

    def __init__(self, game: Game):
        super().__init__(image="bacpack_1.png", kind="backpack_level_1", game=game)
        self.capacity = 1
        self.image_in_hands = "bacpack_1.png"



class Backpack2(Backpack0):
    """ рюкзак """

    def __init__(self, game: Game):
        super().__init__(image="bacpack_2.png", kind="backpack_level_2", game=game)
        self.capacity = 2
        self.image_in_hands = "bacpack_2.png"



class Backpack3(Backpack0):
    """ рюкзак """

    def __init__(self, game: Game):
        super().__init__(image="bacpack_3.png", kind="backpack_level_3", game=game)
        self.capacity = 3
        self.image_in_hands = "bacpack_3.png"



# =====  MEDICINE  ==========================================================

class Medicine(Items):
    """ Класс-родитель для лекарств """

    def __init__(self, image: str, kind: str, game: Game):
        super().__init__(image=image, kind_0="medicine",image2="U.Z.I_in_hands.png", kind=kind, game=game)
        self.heal = 0
        self.heal_target = ""



class Medikit(Medicine):
    """ лекарство """

    def __init__(self, game: Game):
        super().__init__(image="medikit.png", kind="Medikit", game=game)
        self.heal = 5
        self.heal_target = "health"
        self.image_in_hands = "medikit.png"



class Cotton(Medicine):
    """ нитки """

    def __init__(self, game: Game):
        super().__init__(image="coath.png", kind="Cotton", game=game)
        self.heal = 1
        self.heal_target = "armor"
        self.image_in_hands = "coath.png"



# =====  FUNCTIONS  ==========================================================

def items_generator(count: int, game: Game) -> list:
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
        random.choice([Medikit, Cotton]),  # Medicine
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
            [LittleCartridge for _ in range(random.randrange(1, 2))],
            [Fraction for _ in range(random.randrange(1, 2))],
            [Medikit for _ in range(random.randrange(1, 3))],
            [Cotton for _ in range(random.randrange(1, 3))],
        ]
        items_extra = [i for l in items_extra for i in l]
        item_extra = random.choice(items_extra)
        item = item_extra(game=game)
        items.append(item)
    return items
