import os
from typing import Optional, NamedTuple, Union

import pygame
from pygame import Rect, Surface
from pygame.sprite import Group

import constants as c
from backpack import Backpack
from controls import Controls
from dashboard import DashboardLeft
from hero import Hero
from map import Map
from monsters import Monster

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
    heroes: Optional[Group] = None  # спрайты с героями
    monsters: Optional[Group] = None  # спрайты с монстрами
    characters: Optional[Group] = None  # спрайты с героями и монстрами
    map: Optional[Map] = None  # карта
    dashboard_left: Optional[DashboardLeft] = None  # приборная панель
    backpack: Optional[Backpack] = None  # рюкзак
    kb_mode: str = "map"  # keyboard mode, map/attack/backpack
    kb_locked: bool = False  # нажата любая кнопка
    # счётчики
    turns_counter: int = 0  # счётчик ходов
    rounds_counter: int = 0  # счетчик кругов
    monster_waves_counter: int = 0  # счетчик волн монстров
    rounds_between_monster_wave: int = 5  # количество кругов между волнами монстров

    def __init__(self, heroes: int, map_id: int):
        """  Создаёт игру
        :param heroes: колличество героев в игре. Если players_count=0, то создаст читера.
        """
        self.screen = self._init_screen()
        self.heroes = self._init_heroes(heroes)
        self.monsters = Group()
        self.characters = self._init_characters()
        self.map = self._init_map(map_id)
        self.dashboard_left = DashboardLeft(self.screen_rect(), self.map)
        self.backpack = Backpack(self)
        self.controls = Controls(self)

    @staticmethod
    def _init_screen() -> Surface:
        """ Создаёт экран игры """
        os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
        screen = pygame.display.set_mode()
        return screen

    def screen_rect(self) -> Rect:
        """ Возвращает прямоугольник экрана """
        screen_w, screen_h = self.screen.get_size()
        screen_rect = Rect(0, 0, screen_w, screen_h)
        return screen_rect

    def _init_heroes(self, count: int) -> Group:
        """ Создаёт группу из героев """
        heroes = Group()

        # герои
        if count:
            attributes = [
                ('hero_1', 'hero1.png', (1, 1), self),
                ('hero_2', 'hero2.png', (1, 2), self),
                ('hero_3', 'hero3.png', (1, 3), self),
                ('hero_4', 'hero4.png', (1, 4), self),
            ][:count]
            for attrs in attributes:
                hero = Hero(*attrs)
                heroes.add(hero)
            # первый герой активный
            hero1 = heroes.sprites()[0]
            hero1.start_turn()
        # читер
        else:
            pass
            # hero = Hero.cheater(self)
            # heroes.add(hero)

        return heroes

    def init_monsters_wave(self) -> None:
        """ Создаёт волну монстров. Добавляет монстров в группу спрайтов. """

        # 1-ая волна монстров
        if self.monster_waves_counter == 1:
            monster1 = Monster.little(name="little_monster_1", cell_xy=[1, 1], game=self)
            self.monsters.add(monster1)
            self.characters.add(monster1)
            self.map.add_characters([monster1])
            return

        # 2-ая волна монстров
        if self.monster_waves_counter == 2:
            monster2 = Monster.little(name="little_monster_2", cell_xy=[13, 1], game=self)
            monster3 = Monster.little(name="little_monster_3", cell_xy=[1, 9], game=self)
            self.monsters.add(monster2, monster3)
            self.characters.add(monster2, monster3)
            self.map.add_characters([monster2, monster3])
            return

        # 3-ая волна монстров
        if self.monster_waves_counter == 3:
            monster4 = Monster.big(name="big_monster_1", cell_xy=[5, 4], game=self)
            self.monsters.add(monster4)
            self.characters.add(monster4)
            self.map.add_characters([monster4])

    def _init_characters(self) -> Group:
        """ Создаёт группу из всех героев и монстров """
        characters = Group()
        for hero in self.heroes:
            characters.add(hero)
        for monster in self.monsters:
            characters.add(monster)
        return characters

    def _init_map(self, map_id: int = 1) -> Map:
        """ Создаёт карту, добавляет на карту героев, монстров, вещи """
        screen_rect = self.screen_rect()
        if map_id == 0:
            map_ = Map(screen_rect, c.MAP_SANDBOX_NO_WALLS)
        elif map_id == 1:
            map_ = Map(screen_rect, c.MAP_1)
        elif map_id == 2:
            map_ = Map(screen_rect, c.MAP_SANDBOX)
        else:
            raise ValueError("не задан map_id")
        map_.add_characters(self.characters)
        map_.add_items_to_map()
        return map_

    def get_active_character(self) -> CharacterHM:
        """ возвращает активного персонажа """
        characters = self.characters.sprites()
        for character in characters:
            if character.active:
                return character
        raise ValueError("нет активного персонажа")

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
        hero = self.get_active_character()
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
                self.backpack.clear_item_id()
                return
            if keys[pygame.K_F1]:
                self.kb_mode = "controls"
                self.backpack.clear_item_id()
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
                hero.pick_up_item()
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
        elif self.kb_mode == 'controls':
            # переключает управление на карту
            if keys[pygame.K_ESCAPE] or keys[pygame.K_F1]:
                self.kb_mode = 'map'
                return
        elif self.kb_mode == 'backpack':
            # переключает управление на карту
            if keys[pygame.K_ESCAPE] or keys[pygame.K_i]:
                self.kb_mode = 'map'
                return
            # выбирает вещь в рюкзаке
            if keys[pygame.K_UP]:
                self.backpack.select_item(pygame.K_UP)
                return
            if keys[pygame.K_DOWN]:
                self.backpack.select_item(pygame.K_DOWN)
                return
            if keys[pygame.K_e]:
                self.backpack.item_to_hands()
                return

        elif self.kb_mode == 'attack':
            if keys[pygame.K_ESCAPE] or keys[pygame.K_a]:
                self.kb_mode = 'map'
                return
            if keys[pygame.K_UP]:
                hero = self.get_active_character()
                hero.attack(pygame.K_UP)
                return
            if keys[pygame.K_DOWN]:
                hero = self.get_active_character()
                hero.attack(pygame.K_DOWN)
                return
            if keys[pygame.K_LEFT]:
                hero = self.get_active_character()
                hero.attack(pygame.K_LEFT)
                return
            if keys[pygame.K_RIGHT]:
                hero = self.get_active_character()
                hero.attack(pygame.K_RIGHT)
                return

    def monster_actions(self) -> None:
        """ двигает монстров """
        if not self.get_active_character().type == "monster":
            return
        monster = self.get_active_character()
        monster.move()
        print(monster.cell_xy[0])

    def draw(self) -> None:
        """ Рисует карту, героев, мрнстров """
        self.screen.fill(c.BLACK)
        # pygame.draw.rect(self.screen, c.GREEN, self.map.rect, 1)
        # pygame.draw.rect(self.screen, c.RED, self.dashboard_left.rect, 10)
        self.map.draw(self.screen)
        self.map.draw_xy_on_map(self.screen)
        # self.map.draw_ii_cells(self.screen)
        self.characters.draw(self.screen)
        self.monsters.draw(self.screen)
        character = self.get_active_character()
        self.dashboard_left.draw(self.screen, character)

        if self.kb_mode == 'backpack':
            self.backpack.draw(self.screen, character)
        if self.kb_mode == 'controls':
            self.controls.draw(self.screen, character)
