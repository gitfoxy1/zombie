import os
from typing import Optional

import pygame
from pygame import Rect, Surface
from pygame.sprite import Group

import constants as c
from backpack import Backpack
from character import Hero
from character import Monster
from controls import Controls
from dashboard import DashboardLeft
from map import Map


class Game:
    """
     dictionary of terms:
     round -
     turn -
     actions -
     """
    screen: Optional[Surface] = None
    heroes: Optional[Group] = None
    monsters: Optional[Group] = None
    characters: Optional[Group] = None
    map: Optional[Map] = None
    dashboard_left: Optional[DashboardLeft] = None
    backpack: Optional[Backpack] = None
    kb_mode: str = "map"  # keyboard mode, карта по умолчанию
    key_pressed: bool = False  # нажата люмая кнопка
    rounds_counter: int = 0  # счетчик кругов
    # когда rounds_counter дойдет до этого значения он сбросится а waves_counter увеличится на 1
    rounds_in_wave: int = 5
    waves_counter: int = 0  # счетчик волн монстров

    def __init__(self, heroes=0, monsters=10):
        """  Создадим игру
        :param heroes: колличество героев в игре. Если players_count=0, то будет читер.
        :param monsters: колличество мончтров в игре.
        """
        self.screen = self._init_screen()
        self.heroes = self._init_heroes(heroes)
        self.monsters = Group()
        self.characters = self._init_characters()
        self.map = self._init_map()
        self.dashboard_left = DashboardLeft(self.screen_rect(), self.map)
        self.backpack = Backpack(self)
        self.controls = Controls(self)

    @staticmethod
    def _init_screen() -> Surface:
        """ Создадим экран игры """
        os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
        screen = pygame.display.set_mode()
        return screen

    def screen_rect(self) -> Rect:
        """ возвращает прямоугольник экрана """
        screen_w, screen_h = self.screen.get_size()
        screen_rect = Rect(0, 0, screen_w, screen_h)
        return screen_rect

    def _init_heroes(self, count: int) -> Group:
        """ Создадим группу из героев """
        heroes = Group()
        attributes = [
            ('hero_1', 'hero1.png', (1, 1), self),
            ('hero_2', 'hero2.png', (1, 2), self),
            ('hero_3', 'hero3.png', (1, 3), self),
            ('hero_4', 'hero4.png', (1, 4), self),
        ]
        for i, attrs in enumerate(attributes):
            heroes.add(Hero(*attrs))
            if count and i + 1 >= count:
                break

        # первый герой активный
        sprites = heroes.sprites()
        sprites[0].active = True
        return heroes

    def _add_monsters(self) -> None:
        """ Создадим группу из монстров """
        wave = self.waves_counter
        if wave:
            if wave == 1:
                monster1 = Monster.little_monster(id_=1, xy=(1, 1), game=self)
                self.monsters.add(monster1)
            if wave == 2:
                monster2 = Monster.little_monster(id_=2, xy=(13, 1), game=self)
                monster3 = Monster.little_monster(id_=3, xy=(1, 9), game=self)
                self.monsters.add(monster3, monster2)
            if wave == 3:
                monster4 = Monster.big_monster(id_=1, xy=(5, 4), game=self)
                self.monsters.add(monster4)

    def _init_characters(self) -> Group:
        """ Создадим группу из всех героев и монстров """
        characters = Group()
        for hero in self.heroes:
            characters.add(hero)
        for monster in self.monsters:
            characters.add(monster)
        return characters

    def _init_map(self) -> Map:
        """ Создадим карту, добавим на карту героев, монстров, вещи """
        screen_rect = self.screen_rect()
        map_ = Map(screen_rect, c.MAP_1)
        map_.add_charecters(self.characters)
        map_.add_items_to_map()
        return map_

    def get_active_character(self) -> Hero:
        """ возвращает активного героя """
        for character in self.characters:
            if character.active:
                return character

    def update_active_character(self) -> bool:
        """ ход переходит к следующему герою """
        characters = self.characters.sprites()
        for i, character in enumerate(characters):
            # пропускаем не активных игроков
            if not character.active:
                continue

            # активный игрок
            # выдодим если действия у активного игрока ещё не закончились
            if character.actions > 0:
                return False
            # действия у активного игрока закончились,
            # меняем активного игрока на следующего в списке
            character.active = False
            character.actions = character.actions_max
            # если есть следующий игрок в списке, то ход переходит следующиму игроку
            if len(characters) > i + 1:
                characters[i + 1].active = True
                return False
            # если это последний игрок в очереди, то ход передаестся первому игроку
            characters[0].active = True
            return True

    def update_rounds_wave_counter(self, is_round_ended: bool) -> None:
        """ обновляем счетчик кругов и волн монстров """
        if is_round_ended:
            self.rounds_counter += 1
            if not self.rounds_counter % self.rounds_in_wave:
                self.waves_counter += 1

    def keys_actions(self) -> None:
        """ В зависимости от нажатой кнопки меняем управление клавиатуры
        по умолчанию - управление на карте
            UP, DOWN, LEFT, RIGH
        F1 - help, описание кнопок
        I - управление на рюкзак
        A - атакуем
         """
        keys = pygame.key.get_pressed()
        is_key_pressed = bool([i for i in keys if i])  # нажата любая кнопка
        # клавиатура уже заморожена, пропускаем проверку кнопок
        if self.key_pressed and is_key_pressed:
            return
        # замораживаем клавиатуру, пока не будут отпущены все кнопки
        self.key_pressed = True

        hero = self.get_active_character()
        if self.kb_mode == "map":
            # меняем режим клавиатуры с карты на рюкзак
            if keys[pygame.K_i]:
                self.kb_mode = "backpack"
                self.backpack.clear_item_id()
                return
            if keys[pygame.K_F1]:
                self.kb_mode = "controls"
                self.backpack.clear_item_id()
                return
            # меняем режим клавиатуры с карты на атаку
            if keys[pygame.K_a]:
                self.kb_mode = "attack"
                return
            # Передвижение персонажа по карте
            elif keys[pygame.K_UP]:
                hero.move(pygame.K_UP)
                return
            elif keys[pygame.K_DOWN]:
                hero.move(pygame.K_DOWN)
                return
            elif keys[pygame.K_LEFT]:
                hero.move(pygame.K_LEFT)
                return
            elif keys[pygame.K_RIGHT]:
                hero.move(pygame.K_RIGHT)
                return
            # герой поднимает вещь на карте
            elif keys[pygame.K_e]:
                hero.pick_up_item()
                return
            elif keys[pygame.K_d]:
                hero.drop_down_item()
                return
            elif keys[pygame.K_w]:
                hero.wear()
                return
            elif keys[pygame.K_u]:
                hero.use()
                return

        # управление в рюкзаке
        elif self.kb_mode == 'controls':
            # переключаем управление на карту
            if keys[pygame.K_ESCAPE] or keys[pygame.K_F1]:
                self.kb_mode = 'map'
                return
        elif self.kb_mode == 'backpack':
            # переключаем управление на карту
            if keys[pygame.K_ESCAPE] or keys[pygame.K_i]:
                self.kb_mode = 'map'
                return
            # выбираем вещь в рюкзаке
            elif keys[pygame.K_UP]:
                self.backpack.select_item(pygame.K_UP)
                return
            elif keys[pygame.K_DOWN]:
                self.backpack.select_item(pygame.K_DOWN)
                return
            elif keys[pygame.K_e]:
                self.backpack.item_to_hands()
                return

        elif self.kb_mode == 'attack':
            if keys[pygame.K_ESCAPE] or keys[pygame.K_a]:
                self.kb_mode = 'map'
                return
            elif keys[pygame.K_UP]:
                hero = self.get_active_character()
                hero.attack(pygame.K_UP)
                return
            elif keys[pygame.K_DOWN]:
                hero = self.get_active_character()
                hero.attack(pygame.K_DOWN)
                return
            elif keys[pygame.K_LEFT]:
                hero = self.get_active_character()
                hero.attack(pygame.K_LEFT)
                return
            elif keys[pygame.K_RIGHT]:
                hero = self.get_active_character()
                hero.attack(pygame.K_RIGHT)
                return

        # у героя закончился ход, ход переходит к следующему герою
        is_round_ended = self.update_active_character()
        self.update_rounds_wave_counter(is_round_ended)
        if is_round_ended and not self.rounds_counter % self.rounds_in_wave:
            self._add_monsters()
        print(self.waves_counter, self.rounds_counter, self.monsters, is_round_ended)
        # размораживаем клавиатуру, ни одна кнопка не нажата
        self.key_pressed = False

    def draw(self) -> None:
        """ Рисуем карту, героев, мрнстров """
        self.screen.fill(c.BLACK)
        # pygame.draw.rect(self.screen, c.GREEN, self.map.rect, 1)
        # pygame.draw.rect(self.screen, c.RED, self.dashboard_left.rect, 10)
        self.map.draw(self.screen)
        self.characters.draw(self.screen)
        self.monsters.draw(self.screen)
        character = self.get_active_character()
        self.dashboard_left.draw(self.screen, character)

        if self.kb_mode == 'backpack':
            self.backpack.draw(self.screen, character)
        if self.kb_mode == 'controls':
            self.controls.draw(self.screen, character)
