""" игра """
import os
from typing import Optional, NamedTuple, Union
from time import sleep
import random

import pygame
from pygame import Rect, Surface
from pygame.sprite import Group

import settings as s
from backpack import Backpack
from controls import Controls
from dashboard import DashboardLeft
from hero import Hero
from map import Map
from monster import Monster
from items import items_generator

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
    rounds_between_monster_wave: int = 1  # количество кругов между волнами монстров

    def __init__(self, map_: str, heroes: int, monsters: int):
        """  Создаёт игру
        :param heroes: колличество героев в игре. Если players_count=0, то создаст читера.
        """
        self.screen = self._init_screen()
        self.characters: Group = Group()
        self.heroes: Group = Group()
        self.monsters: Group = Group()
        self.map = self._init_map(map_)
        self._init_heroes(heroes)
        self._init_monsters(monsters)
        self._init_items()
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
            dict(xy=(2, 1), game=self),
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

    def _start_turn(self):
        """ перый персонаж в списке спрайтов начинает игру (становится активный) """
        characters = self.characters.sprites()
        if characters:
            character = characters[0]
            character.start_turn()

    def _init_items(self) -> None:
        """ Создаёт и помещает вещи на карту """
        # сгенерим вещи в нужном количестве и добавим в спрйты и на карту
        self.items = Group()
        items = items_generator(count=20)
        for item in items:
            self.items.add(item)
            # добавим вещи на карту
            cell = random.choice(self.map.cells)
            item.xy = cell.xy
            item.update_rect_on_map()  # Sprite.rect
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
            self.monsters.add(monster9)
            self.characters.add(monster9)
            self.map.add_characters([monster9])

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
            monster16 = Monster.little(xy=(2, 6), game=self)
            monster17 = Monster.little(xy=(12, 2), game=self)
            self.monsters.add(monster14, monster15, monster16, monster17, monster19)
            self.characters.add(monster14, monster15, monster16, monster17, monster19)
            self.map.add_characters([monster14, monster15, monster16, monster17, monster19])

        # 9-ая волна монстров
        if self.monster_waves_counter == 9:
            monster24 = Monster.eye(xy=(7, 3), game=self)
            monster23 = Monster.big(xy=(6, 3), game=self)
            monster22 = Monster.big(xy=(4, 9), game=self)
            monster21 = Monster.little(xy=(4, 6), game=self)
            monster20 = Monster.little(xy=(2, 9), game=self)
            self.monsters.add(monster20, monster21, monster22, monster23, monster24)
            self.characters.add(monster20, monster21, monster22, monster23, monster24)
            self.map.add_characters([monster20, monster21, monster22, monster23, monster24])

        # 10-ая волна монстров
        if self.monster_waves_counter == 10:
            monster25 = Monster.eye(xy=(1, 4), game=self)
            monster29 = Monster.fast(xy=(3, 2), game=self)
            monster26 = Monster.big(xy=(7, 6), game=self)
            monster27 = Monster.big(xy=(9, 9), game=self)
            monster28 = Monster.big(xy=(5, 9), game=self)
            self.monsters.add(monster25, monster26, monster27, monster28, monster29)
            self.characters.add(monster25, monster26, monster27, monster28, monster29)
            self.map.add_characters([monster25, monster26, monster27, monster28, monster29])

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
            self.monsters.add(monster33)
            self.characters.add(monster33)
            self.map.add_characters([monster33])

        # 13-ая волна монстров
        if self.monster_waves_counter == 13:
            monster34 = Monster.shooting(xy=(10, 2), game=self)
            monster38 = Monster.eye(xy=(4, 1), game=self)
            monster39 = Monster.eye(xy=(3, 5), game=self)
            monster37 = Monster.fast(xy=(3, 2), game=self)
            monster35 = Monster.little(xy=(12, 2), game=self)
            monster36 = Monster.little(xy=(6, 1), game=self)
            self.monsters.add(monster34, monster35, monster36, monster37, monster38, monster39)
            self.characters.add(monster34, monster35, monster36, monster37, monster38, monster39)
            self.map.add_characters([monster34, monster35, monster36, monster37, monster38, monster39])

        # 14-ая волна монстров
        if self.monster_waves_counter == 14:
            monster40 = Monster.shooting(xy=(10, 2), game=self)
            monster41 = Monster.shooting(xy=(10, 2), game=self)
            monster42 = Monster.eye(xy=(4, 1), game=self)
            monster43 = Monster.eye(xy=(3, 5), game=self)
            monster44 = Monster.fast(xy=(3, 2), game=self)
            monster45 = Monster.fast(xy=(3, 2), game=self)
            monster46 = Monster.big(xy=(5, 9), game=self)
            self.monsters.add(monster40, monster41, monster42, monster43, monster44, monster45, monster46)
            self.characters.add(monster40, monster41, monster42, monster43, monster44, monster45, monster46)
            self.map.add_characters([monster40, monster41, monster42, monster43, monster44, monster45, monster46])


        # 15-ая волна монстров
        if self.monster_waves_counter == 15:
            monster52 = Monster.smart(xy=(14, 9), game=self)
            monster51 = Monster.eye(xy=(7, 5), game=self)
            monster50 = Monster.eye(xy=(5, 7), game=self)
            monster49 = Monster.eye(xy=(2, 9), game=self)
            monster48 = Monster.big(xy=(7, 7), game=self)
            monster47 = Monster.little(xy=(6, 6), game=self)
            self.monsters.add(monster47, monster48, monster49, monster50, monster51, monster52)
            self.characters.add(monster47, monster48, monster49, monster50, monster51, monster52)
            self.map.add_characters([monster47, monster48, monster49, monster50, monster51, monster52])


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
        self.map.draw_xy(self.screen)
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

    def draw_game_over(self) -> None:
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
