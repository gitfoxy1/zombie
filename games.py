""" игра """
import os
import random
from datetime import datetime
from typing import Optional, NamedTuple, Union

import pygame
from pygame import Rect, Surface
from pygame.sprite import Group

import settings as s
from backpack import Backpack
from controls import Controls
from dashboard import DashboardLeft
from hero import Hero
from items import items_generator
from map import Map
from monster import Monster
from pygame.mixer import Sound, Channel

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
    screen: Optional[Surface] = None
    map: Optional[Map] = None  # карта
    heroes: Optional[Group] = None  # спрайты с героями
    monsters: Optional[Group] = None  # спрайты с монстрами
    characters: Optional[Group] = None  # спрайты с героями и монстрами
    items: Optional[Group] = None  # спрайты с вещами
    dashboard_left: Optional[DashboardLeft] = None  # приборная панель
    backpack: Optional[Backpack] = None  # рюкзак
    kb_mode: str = "map"  # keyboard mode, map/attack/backpack
    kb_locked: bool = False  # нажата любая кнопка
    # счётчики
    turns_counter: int = 0  # счётчик ходов
    rounds_counter: int = 0  # счетчик кругов
    monster_waves_counter: int = 0  # счетчик волн монстров
    rounds_between_monster_wave: int = 5  # количество кругов между волнами монстров
    is_game_over = False  # TODO

    def __init__(self, map_: str, heroes: int, monsters: int, items: int):
        """  Создаёт игру
        :param heroes: колличество героев в игре. Если players_count=0, то создаст читера.
        """
        self.start_time = datetime.now()
        self.screen = self._init_screen()
        self.characters: Group = Group()
        self.heroes: Group = Group()
        self.monsters: Group = Group()
        self.map = self._init_map(map_)
        self._init_heroes(heroes)
        self._init_monsters(monsters)
        self._init_items(items)
        self._start_turn()

        self.dashboard_left = DashboardLeft(self.get_screen_rect(), self.map)
        self.backpack = Backpack(self)
        self.controls = Controls(self)
        self.max_x = 14
        self.max_y = 9

    @staticmethod
    def _init_screen() -> Surface:
        """ Создаёт экран игры """
        os.environ["SDL_VIDEO_WINDOW_POS"] = "0,0"
        screen = pygame.display.set_mode()
        return screen

    def get_screen_rect(self) -> Rect:
        """ return прямоугольник экрана """
        screen_w, screen_h = self.screen.get_size()
        screen_rect = Rect(0, 0, screen_w, screen_h)
        return screen_rect

    def _init_map(self, name: str = None) -> Map:
        """ Создаёт карту """
        if name == "SANDBOX_NO_WALLS":
            map_ = Map(name="SANDBOX_NO_WALLS", ascii_=s.MAP_SANDBOX_NO_WALLS, game=self)
        elif name == "MAP1":
            map_ = Map(name="MAP1", ascii_=s.MAP_1, game=self)
        elif name == "SANDBOX":
            map_ = Map(name="SANDBOX", ascii_=s.MAP_SANDBOX, game=self)
        else:
            map_ = Map(name="SANDBOX_NO_WALLS", ascii_=s.MAP_SANDBOX_NO_WALLS, game=self)
        return map_

    def _init_heroes(self, count: int) -> None:
        """ Создаёт группу из героев, добавляет на карту, в список спрайтов """
        self.heroes = Group()
        for i, attrs in enumerate([
            dict(name="hero_1", image="hero1.png", xy=(12, 9), game=self),
            dict(name="hero_2", image="hero2.png", xy=(1, 2), game=self),
            dict(name="hero_3", image="hero3.png", xy=(1, 3), game=self),
            dict(name="hero_4", image="hero4.png", xy=(1, 4), game=self),
        ]):
            if i >= count:
                break
            hero = Hero(**attrs)  # создадим героя
            self.heroes.add(hero)  # добавим героя в спрайты героев
            self.characters.add(hero)  # добавим героя в спрайты персонажей
            cell = self.map.get_cell(attrs["xy"])  # добавим героя на карту
            cell.characters.append(hero)

    def _init_monsters(self, count: int) -> None:
        """ Создаёт группу из монстров, добавляет на карту, в список спрайтов """
        self.monsters = Group()
        for i, attrs in enumerate([
            dict(xy=(13, 7), game=self),
            dict(xy=(2, 2), game=self),
            dict(xy=(2, 3), game=self),
            dict(xy=(2, 4), game=self),
        ]):
            if i >= count:
                break
            monster = Monster.little(**attrs)  # создадим монстра
            self.monsters.add(monster)  # добавим монстра в спрайты монстрв
            self.characters.add(monster)  # добавим монстра в спрайты персонажей
            cell = self.map.get_cell(attrs["xy"])  # добавим монстра на карту
            cell.characters.append(monster)

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
        self.map.draw(self.screen)
        # дропаем вещи на карту
        items = self.items.sprites()
        count = int(len(items) * (1 - alpha / alpha_max))
        items = items[:count]
        items_group = Group()
        items_group.add(items)
        print(count)
        items_group.draw(self.screen)
        # карта появляется из темноты
        rect = self.get_screen_rect()
        surface = pygame.Surface(rect.bottomright)
        surface.set_alpha(alpha)
        surface.fill(s.BLACK)
        self.screen.blit(surface, rect.topleft)
        if alpha <= 0:
            return False
        return True

    def _start_turn(self):
        """ перый персонаж в списке спрайтов начинает игру (становится активный) """
        characters = self.characters.sprites()
        if characters:
            character = characters[0]
            character.start_turn()

    def _init_items(self, count: int) -> None:
        """ Создаёт и помещает вещи на карту """
        # сгенерим вещи в нужном количестве и добавим в спрйты и на карту
        self.items = Group()
        items = items_generator(count=count)
        for item in items:
            self.items.add(item)
            # добавим вещи на карту
            cell = random.choice(self.map.cells)
            item.xy = cell.xy
            item.update_rect()  # Sprite.rect
            cell.items.append(item)

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

    def get_active_character(self) -> CharacterHM:
        """ возвращает активного персонажа """
        characters = self.characters.sprites()
        for character in characters:
            if character.active:
                return character
        raise ValueError("нет активного персонажа")

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

    def is_characters_in_cell(self) -> bool:
        for character in self.characters:
            cell = self.map.get_cell(character.xy)
            if character.rect.center != cell.rect.center:
                return False
        return True

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
        # pygame.draw.rect(self.screen, s.GREEN, self.map.rect, 1)
        # pygame.draw.rect(self.screen, s.RED, self.dashboard_left.rect, 10)
        self.map.draw(self.screen)
        # self.map.draw_xy(self.screen)
        self.items.draw(self.screen)
        self.characters.draw(self.screen)
        # self.draw_monster_path()
        character = self.get_active_character()
        self.dashboard_left.draw(self.screen, character)

        if self.kb_mode == "backpack":
            self.backpack.draw(self.screen, character)
        if self.kb_mode == "controls":
            self.controls.draw(self.screen)

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
        #     sleep(0.01)
        # sleep(1)

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
