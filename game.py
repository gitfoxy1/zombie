""" игра """
import random
from datetime import datetime
from typing import Optional, NamedTuple, Tuple, Union
import os

import pygame
from pygame import Surface
from pygame.mixer import Sound, Channel
from pygame.sprite import Group

import settings as s

from backpack import Backpack
from controls import Controls
from dashboard import Dashboard
from hero import Hero
from items import items_generator
from map import Map
from monster import Monster
import time
from text import Text


CharacterHM = Union[Hero, Monster]


class Counters(NamedTuple):
    """ Состояния счётчиков после каждого turn/хода """
    turn: bool
    round: bool
    wave: bool


class Game:
    """
     Термины:
     round - Круг. За один круг все персонажи делают по одному ходу.
     turn - Ход. За один ход, персонаж делает заданное количество действий.
     action - Действиею Переход на соседнюю клетку, атака.
     """
    kb_mode: str = "controls"  # keyboard mode, map/attack/backpack
    kb_locked: bool = False  # нажата любая кнопка
    # счётчики
    turns_counter: int = 0  # счётчик ходов
    rounds_counter: int = 0  # счетчик кругов
    monster_waves_counter: int = 0  # счетчик волн монстров
    rounds_between_monster_wave: int = 1  # количество кругов между волнами монстров
    is_world_motion = False  # происходит сдвиг игрового мира
    is_game_over = False
    world_shift = (0, 0)

    def __init__(self, map_: str, heroes: int, monsters: int, items: int):
        """  Создаёт игру
        :param heroes: колличество героев в игре. Если players_count=0, то создаст читера.
        """
        self.start_time = datetime.now()
        self.screen = self._init_screen()
        # map
        self.map: Map = self._init_map(map_)  # карта
        self.maps: Group = Group(self.map)
        # sprites
        self.characters: Group = Group()  # спрайты с героями и монстрами
        self.heroes: Group = self._init_heroes(heroes)  # спрайты с героями
        self.monsters: Group = self._init_monsters(monsters)  # спрайты с монстрами
        self.items: Group = self._init_items(items)  # спрайты с вещами

        self._start_turn()
        self.dashboard = Dashboard(self)  # приборная панель
        self.backpack: Backpack = Backpack(self)  # рюкзак
        self.controls: Controls = Controls(self)  # help
        self.monsters_killed = 0

    @staticmethod
    def _init_screen() -> Surface:
        """ Создаёт экран игры """
        if s.SCREEN_SIZE[0] and s.SCREEN_SIZE[1]:  # окно
            screen = pygame.display.set_mode((s.SCREEN_SIZE[0], s.SCREEN_SIZE[1]))
        else:
            os.environ["SDL_VIDEO_WINDOW_POS"] = "0,0"  # полноэкранный режим
            screen = pygame.display.set_mode()
        return screen

    def _init_map(self, name: str = None) -> Map:
        """ Создаёт карту """
        if name == "map":
            map_ = Map(name=name, ascii_=s.MAP_1, game=self)
        elif name == "SANDBOX":
            map_ = Map(name="SANDBOX", ascii_=s.MAP_SANDBOX, game=self)
        else:
            map_ = Map(name="SANDBOX_NO_WALLS", ascii_=s.MAP_SANDBOX_NO_WALLS, game=self)
        return map_

    def _init_heroes(self, count: int) -> Group:
        """ Создаёт группу из героев, добавляет на карту, в список спрайтов
        если count=0, спросит количество героев """
        if not count:
            count = 1
        heroes = Group()
        attrs = [
            dict(name="hero1", image="hero1.png", xy=(12, 8), game=self),
            dict(name="hero2", image="hero2.png", xy=(1, 2), game=self),
            dict(name="hero3", image="hero3.png", xy=(1, 3), game=self),
            dict(name="hero4", image="hero4.png", xy=(1, 4), game=self),
        ][:count]
        for attr in attrs:
            hero = Hero(**attr)  # создадим героя
            heroes.add(hero)  # добавим героя в спрайты героев
            self.characters.add(hero)  # добавим героя в спрайты персонажей
            cell = self.map.get_cell(attr["xy"])  # добавим героя на карту
            cell.characters.append(hero)
        return heroes

    def _init_monsters(self, count: int) -> Group:
        """ Создаёт группу из монстров, добавляет на карту, в список спрайтов """
        monsters = Group()
        attrs = [
            dict(xy=(13, 7), game=self),
            dict(xy=(13, 7), game=self),
            dict(xy=(13, 7), game=self),
            dict(xy=(2, 4), game=self),
        ][:count]
        for attr in attrs:
            monster = Monster.little(**attr)  # создадим монстра
            monsters.add(monster)  # добавим монстра в спрайты монстрв
            self.characters.add(monster)  # добавим монстра в спрайты персонажей
            cell = self.map.get_cell(attr["xy"])  # добавим монстра на карту
            cell.characters.append(monster)
        return monsters

    def _init_items(self, count: int) -> Group:
        """ Создаёт и помещает вещи на карту """
        # сгенерим вещи в нужном количестве и добавим в спрйты и на карту
        items = Group()
        items_ = items_generator(count=count, game=self)
        for item in items_:
            items.add(item)
            # добавим вещи на карту
            cell = random.choice(self.map.cells)
            cell.items.append(item)
            item.xy = cell.xy
            item.update_rect()  # Sprite.rect
        return items

    def intro(self) -> bool:
        """ заставка перед игрой, карта появляется из темноты
         return True пока полностью не появится """
        # прозрачность

        time_delta = datetime.now() - self.start_time
        seconds = time_delta.seconds + time_delta.microseconds / 1000000
        alpha_max = (256 + 100)
        alpha = int(alpha_max - seconds * 30)  # прозрачность > 256 = black
        # рисуем карту
        self.screen.fill(s.BLACK)
        self.maps.draw(self.screen)
        # дропаем вещи на карту
        items = self.items.sprites()
        count = int(len(items) * (1 - alpha / alpha_max))
        items = items[:count]
        items_group = Group()
        items_group.add(items)
        items_group.draw(self.screen)
        # карта появляется из темноты
        screen_rect = self.screen.get_rect()
        surface = pygame.Surface(screen_rect.bottomright)
        surface.set_alpha(alpha * 5)
        surface.fill(s.BROUN)
        self.screen.blit(surface, screen_rect.topleft)
        widht = min(self.screen.get_rect().size)
        size = (widht, widht)
        surface = pygame.image.load(s.I_ZASTAVKA).convert()
        surface = pygame.transform.scale(surface, size)
        rect = surface.get_rect()
        rect.center = self.screen.get_rect().center
        surface.set_alpha(alpha)
        self.screen.blit(surface, rect.topleft)
        # карта появилась
        if alpha <= 0:
            return False
        # карта ещё не появилась
        return True

    def _start_turn(self):
        """ перый персонаж в списке спрайтов начинает игру (становится активный) """
        characters = self.characters.sprites()
        if characters:
            character = characters[0]
            character.start_turn()

    def _init_monsters_wave(self) -> None:
        """ Создаёт волну монстров. Добавляет монстров в группу спрайтов. """

        # 1-ая волна монстров
        if self.monster_waves_counter == 1:
            monster1 = Monster.little(xy=(1, 1), game=self)
            self.monsters.add(monster1)
            self.characters.add(monster1)
            self.map.add_characters([monster1])
            return

        # 2-ая волна монстров
        if self.monster_waves_counter == 2:
            monster2 = Monster.little(xy=(13, 1), game=self)
            monster3 = Monster.little(xy=(1, 9), game=self)
            self.monsters.add(monster2, monster3)
            self.characters.add(monster2, monster3)
            self.map.add_characters([monster2, monster3])
            return

        # 3-ая волна монстров
        if self.monster_waves_counter == 3:
            monster4 = Monster.big(xy=(5, 4), game=self)
            self.monsters.add(monster4)
            self.characters.add(monster4)
            self.map.add_characters([monster4])

        # 4-ая волна монстров
        if self.monster_waves_counter == 4:
            monster5 = Monster.big(xy=(10, 8), game=self)
            monster6 = Monster.little(xy=(3, 3), game=self)
            self.monsters.add(monster5, monster6)
            self.characters.add(monster5, monster6)
            self.map.add_characters([monster5, monster6])

        # 5-ая волна монстров
        if self.monster_waves_counter == 5:
            monster7 = Monster.big(xy=(7, 1), game=self)
            monster8 = Monster.little(xy=(6, 6), game=self)
            self.monsters.add(monster7, monster8)
            self.characters.add(monster7, monster8)
            self.map.add_characters([monster7, monster8])

        # 6-ая волна монстров
        if self.monster_waves_counter == 6:
            monster9 = Monster.boss_1(xy=(11, 8), game=self)
            monster7_ = Monster.big(xy=(7, 1), game=self)
            self.monsters.add(monster9, monster7_)
            self.characters.add(monster9, monster7_)
            self.map.add_characters([monster9, monster7_])

        # 7-ая волна монстров
        if self.monster_waves_counter == 7:
            monster10 = Monster.fast(xy=(2, 5), game=self)
            monster11 = Monster.big(xy=(9, 9), game=self)
            monster12 = Monster.little(xy=(8, 4), game=self)
            self.monsters.add(monster10, monster11, monster12)
            self.characters.add(monster10, monster11, monster12)
            self.map.add_characters([monster10, monster11, monster12])

        # 8-ая волна монстров
        if self.monster_waves_counter == 8:
            monster14 = Monster.fast(xy=(5, 8), game=self)
            monster19 = Monster.fast(xy=(10, 2), game=self)
            monster15 = Monster.big(xy=(3, 9), game=self)
            self.monsters.add(monster14, monster15, monster19)
            self.characters.add(monster14, monster15, monster19)
            self.map.add_characters([monster14, monster15, monster19])

        # 9-ая волна монстров
        if self.monster_waves_counter == 9:
            monster24 = Monster.eye(xy=(7, 3), game=self)
            monster23 = Monster.big(xy=(6, 3), game=self)
            monster21 = Monster.little(xy=(4, 6), game=self)
            self.monsters.add(monster21, monster23, monster24)
            self.characters.add(monster21, monster23, monster24)
            self.map.add_characters([monster21, monster23, monster24])

        # 10-ая волна монстров
        if self.monster_waves_counter == 10:
            monster25 = Monster.eye(xy=(1, 4), game=self)
            monster29 = Monster.fast(xy=(3, 2), game=self)
            monster28 = Monster.little(xy=(9, 6), game=self)
            self.monsters.add(monster25, monster28)
            self.characters.add(monster25, monster28, monster29)
            self.map.add_characters([monster25, monster28, monster29])

        # 11-ая волна монстров
        if self.monster_waves_counter == 11:
            monster31 = Monster.eye(xy=(1, 4), game=self)
            monster30 = Monster.eye(xy=(1, 4), game=self)
            monster32 = Monster.little(xy=(12, 2), game=self)
            self.monsters.add(monster30, monster31, monster32)
            self.characters.add(monster30, monster31, monster32)
            self.map.add_characters([monster30, monster31, monster32])

        # 12-ая волна монстров
        if self.monster_waves_counter == 12:
            monster33 = Monster.boss_2(xy=(9, 8), game=self)
            monster17 = Monster.fast(xy=(3, 2), game=self)
            monster18 = Monster.big(xy=(6, 3), game=self)
            self.monsters.add(monster33, monster17, monster18)
            self.characters.add(monster33, monster17, monster18)
            self.map.add_characters([monster33, monster17, monster18])

        # 13-ая волна монстров
        if self.monster_waves_counter == 13:
            monster34 = Monster.shooting(xy=(10, 2), game=self)
            monster38 = Monster.eye(xy=(4, 1), game=self)
            monster37 = Monster.fast(xy=(3, 2), game=self)
            monster35 = Monster.little(xy=(12, 2), game=self)
            self.monsters.add(monster34, monster35, monster37, monster38)
            self.characters.add(monster34, monster35, monster37, monster38)
            self.map.add_characters(
                [monster34, monster35, monster37, monster38])

        # 14-ая волна монстров
        if self.monster_waves_counter == 14:
            monster40 = Monster.shooting(xy=(10, 2), game=self)
            monster41 = Monster.shooting(xy=(10, 2), game=self)
            monster42 = Monster.eye(xy=(4, 1), game=self)
            monster43 = Monster.eye(xy=(3, 5), game=self)
            self.monsters.add(monster40, monster41, monster42, monster43)
            self.characters.add(monster40, monster41, monster42, monster43)
            self.map.add_characters(
                [monster40, monster41, monster42, monster43])

        # 15-ая волна монстров
        if self.monster_waves_counter == 15:
            monster52 = Monster.smart(xy=(14, 9), game=self)
            monster51 = Monster.fast(xy=(7, 5), game=self)
            monster48 = Monster.little(xy=(7, 7), game=self)
            monster47 = Monster.little(xy=(6, 6), game=self)
            self.monsters.add(monster47, monster48, monster51, monster52)
            self.characters.add(monster47, monster48, monster51, monster52)
            self.map.add_characters(
                [monster47, monster48, monster51, monster52])

        # 16-ая волна монстров
        if self.monster_waves_counter == 16:
            monster53 = Monster.smart(xy=(7, 5), game=self)
            monster54 = Monster.shooting(xy=(5, 4), game=self)
            monster55 = Monster.fast(xy=(14, 9), game=self)
            monster56 = Monster.big(xy=(12, 6), game=self)
            self.monsters.add(monster56, monster54, monster55, monster53)
            self.characters.add(monster56, monster54, monster55, monster53)
            self.map.add_characters(
                [monster56, monster54, monster55, monster53])

        # 17-ая волна монстров
        if self.monster_waves_counter == 17:
            monster57 = Monster.smart(xy=(3, 8), game=self)
            monster58 = Monster.smart(xy=(11, 4), game=self)
            monster59 = Monster.eye(xy=(1, 7), game=self)
            monster60 = Monster.little(xy=(1, 1), game=self)
            self.monsters.add(monster57, monster58, monster59, monster60)
            self.characters.add(monster57, monster58, monster59, monster60)
            self.map.add_characters(
                [monster57, monster58, monster59, monster60])

        # 18-ая волна монстров
        if self.monster_waves_counter == 18:
            monster61 = Monster.boss_3(xy=(6, 6), game=self)
            monster62 = Monster.shooting(xy=(0, 0), game=self)
            monster63 = Monster.eye(xy=(7, 2), game=self)
            monster64 = Monster.little(xy=(4, 9), game=self)
            self.monsters.add(monster61, monster62, monster63, monster64)
            self.characters.add(monster61, monster62, monster63, monster64)
            self.map.add_characters(
                [monster61, monster62, monster63, monster64])

        # 19-ая волна монстров
        if self.monster_waves_counter == 19:
            monster65 = Monster.walking(xy=(3, 1), game=self)
            monster66 = Monster.shooting(xy=(6, 2), game=self)
            monster67 = Monster.shooting(xy=(3, 9), game=self)
            monster68 = Monster.fast(xy=(12, 3), game=self)
            monster69 = Monster.big(xy=(7, 5), game=self)
            self.monsters.add(monster65, monster66, monster67, monster68, monster69)
            self.characters.add(monster65, monster66, monster67, monster68, monster69)
            self.map.add_characters(
                [monster65, monster67, monster66, monster68, monster69])

        # 20-ая волна монстров
        if self.monster_waves_counter == 20:
            monster70 = Monster.walking(xy=(13, 6), game=self)
            monster71 = Monster.walking(xy=(14, 7), game=self)
            monster72 = Monster.smart(xy=(12, 8), game=self)
            monster73 = Monster.fast(xy=(11, 9), game=self)
            monster74 = Monster.little(xy=(10, 5), game=self)
            self.monsters.add(monster70, monster71, monster72, monster73, monster74)
            self.characters.add(monster70, monster71, monster72, monster73, monster74)
            self.map.add_characters(
                [monster70, monster71, monster72, monster73, monster74])

        # 21-ая волна монстров
        if self.monster_waves_counter == 21:
            monster75 = Monster.ghost(xy=(13, 6), game=self)
            monster76 = Monster.smart(xy=(12, 8), game=self)
            monster77 = Monster.fast(xy=(11, 9), game=self)
            monster78 = Monster.little(xy=(10, 5), game=self)
            monster79 = Monster.little(xy=(10, 5), game=self)
            self.monsters.add(monster75, monster76, monster77, monster78, monster79)
            self.characters.add(monster75, monster76, monster77, monster78, monster79)
            self.map.add_characters(
                [monster75, monster77, monster76, monster78, monster79])

        # 22-ая волна монстров
        if self.monster_waves_counter == 22:
            monster80 = Monster.ghost(xy=(3, 2), game=self)
            monster81 = Monster.walking(xy=(1, 9), game=self)
            monster82 = Monster.shooting(xy=(4, 2), game=self)
            monster83 = Monster.eye(xy=(4, 4), game=self)
            monster84 = Monster.big(xy=(8, 8), game=self)
            self.monsters.add(monster80, monster81, monster82, monster83, monster84)
            self.characters.add(monster80, monster81, monster82, monster83, monster84)
            self.map.add_characters(
                [monster80, monster81, monster82, monster83, monster84])

        # 23-ая волна монстров
        if self.monster_waves_counter == 23:
            monster85 = Monster.ghost(xy=(13, 6), game=self)
            monster86 = Monster.walking(xy=(13, 6), game=self)
            monster87 = Monster.shooting(xy=(3, 9), game=self)
            monster88 = Monster.fast(xy=(11, 9), game=self)
            monster89 = Monster.little(xy=(10, 5), game=self)
            self.monsters.add(monster85, monster86, monster87, monster88, monster89)
            self.characters.add(monster85, monster86, monster87, monster88, monster89)
            self.map.add_characters(
                [monster85, monster86, monster87, monster88, monster89])

        # 24-ая волна монстров
        if self.monster_waves_counter == 24:
            monster91 = Monster.boss_4(xy=(2, 9), game=self)
            monster92 = Monster.ghost(xy=(2, 1), game=self)
            monster93 = Monster.shooting(xy=(5, 2), game=self)
            monster94 = Monster.eye(xy=(13, 5), game=self)
            monster90 = Monster.big(xy=(12, 7), game=self)
            self.monsters.add(monster90, monster91, monster92, monster93, monster94)
            self.characters.add(monster90, monster91, monster92, monster93, monster94)
            self.map.add_characters(
                [monster90, monster91, monster92, monster93, monster94])

        # 25-ая волна монстров
        if self.monster_waves_counter == 25:
            monster100 = Monster.bat(xy=(4, 8), game=self)
            monster96 = Monster.walking(xy=(8, 2), game=self)
            monster97 = Monster.smart(xy=(3, 7), game=self)
            monster98 = Monster.fast(xy=(10, 1), game=self)
            monster99 = Monster.fast(xy=(1, 2), game=self)
            monster95 = Monster.little(xy=(0, 0), game=self)
            self.monsters.add(monster95, monster99, monster98, monster97, monster96, monster100)
            self.characters.add(monster95, monster99, monster98, monster97, monster96, monster100)
            self.map.add_characters(
                [monster95, monster99, monster98, monster96, monster97, monster100])

        # 26-ая волна монстров
        if self.monster_waves_counter == 26:
            monster101 = Monster.bat(xy=(3, 6), game=self)
            monster102 = Monster.bat(xy=(13, 3), game=self)
            monster103 = Monster.ghost(xy=(12, 2), game=self)
            monster104 = Monster.shooting(xy=(1, 9), game=self)
            monster105 = Monster.eye(xy=(13, 1), game=self)
            monster106 = Monster.little(xy=(8, 6), game=self)
            self.monsters.add(monster101, monster102, monster103, monster104, monster105, monster106)
            self.characters.add(monster101, monster102, monster103, monster104, monster105, monster106)
            self.map.add_characters(
                [monster101, monster102, monster103, monster104, monster105, monster106])

        # 27-ая волна монстров
        if self.monster_waves_counter == 27:
            monster112 = Monster.vampier(xy=(1, 4), game=self)
            monster111 = Monster.walking(xy=(9, 1), game=self)
            monster110 = Monster.smart(xy=(0, 9), game=self)
            monster109 = Monster.fast(xy=(14, 9), game=self)
            monster108 = Monster.big(xy=(13, 2), game=self)
            monster107 = Monster.little(xy=(2, 2), game=self)
            self.monsters.add(monster107, monster108, monster109, monster110, monster111, monster112)
            self.characters.add(monster107, monster108, monster109, monster110, monster111, monster112)
            self.map.add_characters(
                [monster107, monster108, monster109, monster110, monster111, monster112])

        # 28-ая волна монстров
        if self.monster_waves_counter == 28:
            monster113 = Monster.vampier(xy=(4, 8), game=self)
            monster114 = Monster.bat(xy=(6, 3), game=self)
            monster115 = Monster.walking(xy=(3, 2), game=self)
            monster116 = Monster.shooting(xy=(1, 9), game=self)
            monster117 = Monster.eye(xy=(10, 2), game=self)
            monster118 = Monster.little(xy=(12, 5), game=self)
            self.monsters.add(monster113, monster114, monster115, monster116, monster117, monster118)
            self.characters.add(monster113, monster114, monster115, monster116, monster117, monster118)
            self.map.add_characters(
                [monster113, monster114, monster115, monster116, monster117, monster118])

        # 29-ая волна монстров
        if self.monster_waves_counter == 29:
            monster124 = Monster.bat(xy=(4, 8), game=self)
            monster123 = Monster.bat(xy=(6, 3), game=self)
            monster122 = Monster.walking(xy=(3, 2), game=self)
            monster121 = Monster.shooting(xy=(1, 9), game=self)
            monster120 = Monster.fast(xy=(10, 2), game=self)
            monster119 = Monster.big(xy=(12, 5), game=self)
            self.monsters.add(monster119, monster120, monster121, monster122, monster123, monster124)
            self.characters.add(monster119, monster120, monster121, monster122, monster123, monster124)
            self.map.add_characters(
                [monster119, monster120, monster121, monster122, monster123, monster124])

        # 30-ая волна монстров
        if self.monster_waves_counter == 30:
            monster130 = Monster.boss_5(xy=(0, 0), game=self)
            monster129 = Monster.vampier(xy=(0, 0), game=self)
            monster128 = Monster.ghost(xy=(0, 0), game=self)
            monster127 = Monster.smart(xy=(0, 0), game=self)
            monster126 = Monster.eye(xy=(0, 0), game=self)
            monster125 = Monster.big(xy=(0, 0), game=self)
            self.monsters.add(monster125, monster126, monster127, monster128, monster129, monster130)
            self.characters.add(monster125, monster126, monster127, monster128, monster129, monster130)
            self.map.add_characters(
                [monster125, monster126, monster127, monster128, monster129, monster130])

    def all_heroes_dead(self) -> bool:
        """ return True если все герои умерли """
        characters = self.characters.sprites()
        heroes = [o for o in characters if o.type == "hero"]
        if heroes:
            return False
        return True

    def get_active_character(self) -> Optional[CharacterHM]:
        """ возвращает активного персонажа """
        characters = self.characters.sprites()
        for character in characters:
            if character.active:
                return character
        return None

    def get_active_hero(self) -> Optional[Hero]:
        """ возвращает активного героя """
        character = self.get_active_character()
        if character.type == "hero":
            return character
        return None

    def get_active_monster(self) -> Optional[Monster]:
        """ возвращает активного монстра """
        character = self.get_active_character()
        if character.type == "monster":
            return character
        return None

    def get_next_character(self) -> CharacterHM:
        """ возвращает следующего персонажа после активного """
        characters = self.characters.sprites()
        characters_count = len(characters)
        # найдём активного персонажа
        for i, character in enumerate(characters):
            if character.active:
                # если активный персонаж не последний в списке, вернём следующего
                if characters_count > i + 1:
                    return characters[i + 1]
                # если активный персонаж последний в списке, вернём первого
                return characters[0]
        raise ValueError("нет активного персонажа")

    def is_motion(self) -> bool:
        """ True  - если хоть один персонаж в движении
            False - если все персонажи закончили движение и стоят в своих клетках
        """
        if self.is_world_motion:
            return True
        characters = self.characters.sprites()
        if not characters:
            return False
        for character in characters:
            cell = character.my_cell()
            if character.rect.center != cell.rect.center:
                return True
        return False

    def update_counters(self) -> Counters:
        """ Меняет активного персонажа и обновляет счётчики.
        Если у персонажа закончился действия/actions, то ход/turn переходит к следующему персонажу,
        Если закончился круг/round, обновим счётчик кругов и волн-монстров,
        """
        # активный персонаж
        active_character = self.get_active_character()

        # выходим если у персонажа ещё не закончился действия/actions
        if active_character.actions > 0:
            return Counters(turn=False, round=False, wave=False)

        # если у персонажа закончился действия/actions, ход/turn переходит к следующему персонажу
        self.turns_counter += 1
        next_character = self.get_next_character()
        active_character.end_turn()
        next_character.start_turn()

        # если закончился круг/round, обновим счётчик кругов, начинает ходить первый игрок
        first_character = self.characters.sprites()[0]
        if next_character == first_character:
            self.rounds_counter += 1
            self.turns_counter = 0

            # если счётчик кругов кратен 5, то обновим счётчик волн-монстров
            if not self.rounds_counter % self.rounds_between_monster_wave:
                self.monster_waves_counter += 1
                # закончилась волн-монстров
                return Counters(turn=True, round=True, wave=True)
            # закончился круг/round
            return Counters(turn=True, round=True, wave=False)
        # закончился ход/turn
        return Counters(turn=True, round=False, wave=False)


    def hero_actions(self) -> None:
        """ В зависимости от нажатой кнопки меняет управление клавиатуры
        по умолчанию - управление на карте
            UP, DOWN, LEFT, RIGHT
        F1 - help, описание кнопок
        I - управление на рюкзак
        A - атакует
         """
        hero = self.get_active_hero()
        if not hero:
            return

        keys = pygame.key.get_pressed()
        is_any_key_pressed = bool([i for i in keys if i])  # нажата любая кнопка

        # если ни одна кнопка не нажата, снимает блокировку клавиатуру
        if not is_any_key_pressed:
            self.kb_locked = False
            return
        # если нажата клавиша и клавиатура заблокирована, то клавиши не проверяем
        if self.kb_locked and is_any_key_pressed:
            return
        # блокирует клавиатуру, пока не будут отпущены все кнопки
        if not self.kb_locked and is_any_key_pressed:
            self.kb_locked = True

        if self.kb_mode == "map":
            # меняет режим клавиатуры с карты на рюкзак
            if keys[pygame.K_i]:
                self.kb_mode = "backpack"
                self.backpack.active_items_id = 0
                return
            if keys[pygame.K_F1]:
                self.kb_mode = "controls"
                self.backpack.active_items_id = 0
                return
            # меняет режим клавиатуры с карты на атаку
            if keys[pygame.K_a]:
                self.kb_mode = "attack"
                return

            # Передвижение персонажа по карте
            if keys[pygame.K_UP]:
                hero.move(pygame.K_UP)
                return
            if keys[pygame.K_DOWN]:
                hero.move(pygame.K_DOWN)
                return
            if keys[pygame.K_LEFT]:
                hero.move(pygame.K_LEFT)
                return
            if keys[pygame.K_RIGHT]:
                hero.move(pygame.K_RIGHT)
                return
            # герой поднимает вещь на карте
            if keys[pygame.K_e]:
                hero.pickup_item()
                return
            if keys[pygame.K_d]:
                hero.drop_down_item()
                return
            if keys[pygame.K_w]:
                hero.wear()
                return
            if keys[pygame.K_u]:
                hero.use()
                return

        # управление в рюкзаке
        elif self.kb_mode == "controls":
            # переключает управление на карту
            if keys[pygame.K_ESCAPE] or keys[pygame.K_F1]:
                self.kb_mode = "map"
                return
        elif self.kb_mode == "backpack":
            # переключает управление на карту
            if keys[pygame.K_ESCAPE] or keys[pygame.K_i]:
                self.kb_mode = "map"
                return
            # выбирает вещь в рюкзаке
            if keys[pygame.K_UP]:
                self.backpack.select_item(pygame.K_UP)
                return
            if keys[pygame.K_DOWN]:
                self.backpack.select_item(pygame.K_DOWN)
                return
            if keys[pygame.K_RETURN]:
                self.backpack.item_to_hands()
                return

        elif self.kb_mode == "attack":
            if keys[pygame.K_ESCAPE] or keys[pygame.K_a]:
                self.kb_mode = "map"
                return
            if keys[pygame.K_UP]:
                hero = self.get_active_hero()
                hero.attack(pygame.K_UP)
                self.kb_mode = "map"
                return
            if keys[pygame.K_DOWN]:
                hero = self.get_active_hero()
                hero.attack(pygame.K_DOWN)
                self.kb_mode = "map"
                return
            if keys[pygame.K_LEFT]:
                hero = self.get_active_hero()
                hero.attack(pygame.K_LEFT)
                self.kb_mode = "map"
                return
            if keys[pygame.K_RIGHT]:
                hero = self.get_active_hero()
                hero.attack(pygame.K_RIGHT)
                self.kb_mode = "map"
                return

    def monster_actions(self) -> None:
        """ двигает монстров """
        monster = self.get_active_monster()
        if not monster:
            return
        monster.move()
        monster.attack()

    def draw(self) -> None:
        """ Рисует карту, героев, мрнстров """
        self.screen.fill(s.BLACK)
        self.maps.draw(self.screen)
        if s.DEBUG:
            # self.map.draw_cells(self.screen)
            self.draw_cells_xy()

        self.items.draw(self.screen)
        self.characters.draw(self.screen)
        self.draw_items_in_hands()
        self.draw_characters_count_in_cell()
        if s.DEBUG:
            self.draw_monster_path()

        # draw dashboard, backpack, controls window
        self.dashboard.draw()
        if self.kb_mode == "backpack":
            self.backpack.draw()
        if self.kb_mode == "controls":
            self.controls.draw()

    def draw_items_in_hands(self):
        """ Рисует вещь в руках героя """
        hero = self.get_active_hero()
        if hero and hero.item_in_hands:
            pic_ = pygame.transform.scale(hero.item_in_hands.image2, (hero.rect.w, hero.rect.h))
            self.screen.blit(pic_, hero.rect.topleft)

    def draw_characters_count_in_cell(self) -> None:
        """ Рисует количество персонажей в клетке"""
        height = 30
        color = s.BLACK
        font = pygame.font.SysFont(pygame.font.get_default_font(), height)
        shift = 5  # сместим текс на есколько пикселей от края клетки

        for cell in self.map.cells:
            count = len(cell.characters)
            if count >= 2:
                render = font.render(str(count), True, color)
                rect = render.get_rect()
                self.screen.blit(render, cell.bottom_right(rect, shift))

    def draw_cells_xy(self) -> None:
        """ рисует на карте координаты клетки xy """
        height = 15
        color = s.BLACK
        font = pygame.font.SysFont(pygame.font.get_default_font(), height)
        shift = 3  # сместим текс на есколько пикселей от края клетки

        for cell in self.map.cells:
            # координаты клетки (x, y): top, left
            render = font.render(f"{cell.xy[0]},{cell.xy[1]}", True, color)
            xy1 = cell.top_left(shift)
            self.screen.blit(render, xy1)

            # координаты экрана (пиксели): bottom, right
            render = font.render(f"{cell.rect.right},{cell.rect.bottom}", True, color)
            rect2 = render.get_rect()
            xy2 = cell.bottom_right(rect2, shift)
            self.screen.blit(render, xy2)

    def draw_monster_path(self) -> None:
        """ рисует на карте путь монстра """
        monster = self.get_active_monster()
        if not monster:
            return
        route = monster.route
        for i_from, cell_from in enumerate(route):
            i_to = i_from + 1
            if i_to >= len(route):
                break
            cell_to = monster.route[i_to]
            pygame.draw.line(self.screen, s.RED, cell_from.center(), cell_to.center(), 10)
            pygame.display.update()

    def game_over(self) -> None:
        """ рисуем надпись GameOver """
        font = pygame.font.SysFont("consolas", 100)
        text = font.render("Game Over", True, s.RED)
        text_rect = text.get_rect()
        text_rect.center = self.map.rect.center

        size = (text_rect.w + 50, text_rect.h + 50)
        background = pygame.Surface(size)
        background.fill(s.BLACK)
        background_rect = background.get_rect()
        background_rect.center = text_rect.center

        self.screen.blit(background, background_rect.topleft)
        self.screen.blit(text, text_rect.topleft)

        # ch2 = Channel(2)
        # Channel(2).play(Sound(s.S_GAME_OVER))
        # import time
        # time.sleep(3)
        if not self.is_game_over:
            Channel(2).play(Sound(s.S_GAME_OVER))
            self.is_game_over = True

    def win(self) -> None:

        text = Text(self.screen)
        text.size = 100
        text.draw_list(['You win', f'you killed {self.monsters_killed} monsters'], 200, 400)
        time.sleep(5)

    def update_sprites(self) -> None:
        """ обновим передвигающиеся спрайты на экране """
        self.shifting_world()
        self.items.update()
        self.characters.update()

    def shifting_world(self):
        """" Выполняем сдвиг игрового мира, персонаж в центре """
        hero = self.get_active_hero()
        if not hero:
            return
        direction = self.sprite_center_out_of_screen(hero)
        if not direction:
            self.is_world_motion = False
            return

        # смещаем мир
        speed = s.SPEED
        self.is_world_motion = True
        map_rect = self.map.rect
        shift_x, shift_y = self.shift_world_direction(direction)

        diff_x = map_rect.x - shift_x
        if diff_x > 0:
            diff_x = min(speed, diff_x)
        elif diff_x < 0:
            diff_x = max(-speed, diff_x)
        diff_y = map_rect.y - shift_y
        if diff_y > 0:
            diff_y = min(speed, diff_y)
        elif diff_y < 0:
            diff_y = max(-speed, diff_y)
        # движение мира закончилось
        if not (diff_x or diff_y):
            return
        # движение мира, смещаем спрайты
        self.world_shift = (shift_x, shift_y)
        map_rect.topleft = (shift_x, shift_y)
        for cell in self.map.cells:
            cell.update_rect()
        for item in self.items:
            item.update_rect()
        for character in self.characters:
            character.update_rect()

    def sprite_center_out_of_screen(self, sprite) -> str:
        """ return direction если спрайт вышел за пределы экрана """
        map_rect = self.map.rect
        if sprite.rect.centerx < 0:
            return "left"
        if sprite.rect.centery < 0:
            return "top"
        if sprite.rect.centerx > map_rect.width:
            return "right"
        if sprite.rect.centery > map_rect.height:
            return "down"
        return ""

    def shift_world_direction(self, direction: str) -> Tuple[int, int]:
        """ return x,y сдвига игрового мира в направлении direction """
        hero = self.get_active_hero()
        cell = hero.my_cell()
        cell_r = cell.rect
        map_rect = self.map.rect
        map_size = self.map.size
        shift = [0, 0]
        if direction == "top":
            shift[0] = self.world_shift[0]
            shift[1] = -((cell.xy[1] + 1) * s.CELL_W - map_rect.height)
        elif direction == "down":
            shift[0] = self.world_shift[0]
            shift[1] = -(cell.xy[1] * s.CELL_W)
        elif direction == "right":
            shift[0] = -(cell.xy[0] * s.CELL_W)
            shift[1] = self.world_shift[1]
        elif direction == "left":
            shift[0] = -((cell.xy[0] + 1) * s.CELL_W - map_rect.width)
            shift[1] = self.world_shift[1]
        if map_size.width - cell_r.x < map_rect.width:
            shift[0] = map_rect.width - map_size.width
        if shift[0] > 0:
            shift[0] = 0
        if map_size.height - cell_r.y < map_rect.height:
            shift[1] = map_rect.height - map_size.height
        if shift[1] > 0:
            shift[1] = 0
        return tuple(shift)
