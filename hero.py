""" Персонаж герой """

import os
import random
from datetime import datetime
from typing import Optional, Tuple

import pygame
from pygame.mixer import Channel, Sound

import settings as s
from character import Character
from items import Digle, Uzi, Kalashnikov, LittleCartridge, HeavyCartridge, Fraction, Mastif, \
    Awp, Medikit, Knife, Armor1, Cotton, Backpack1

import functions as f

Game = "Game"


class Hero(Character):
    """ Герой """
    items: list = []  # вещи в рюкзаке
    armor: Optional[Armor1] = None  # броня
    armor_points: int = 0  # броня
    backpack: Optional[Backpack1] = None  # рюкзак вещи
    backpack_points: int = 0  # расширение рюкзака
    key_pressed: int = 0  # нажатая клавиша

    # noinspection PyUnresolvedReferences
    def __init__(self, name: str, image: str, xy: Tuple[int, int], game: Game):
        """ делает героя
        @param name: имя героя
        @param image: картинка героя
        @param xy: координаты героя на карте/map
        @param game: ссылка на игру
        """
        super().__init__(name, image, xy, game)
        self.type = "hero"
        self.items = []
        self.armor = None
        self.armor_points = 0
        self.backpack = None
        self.backpack_points = 0
        if self.backpack:
            self.backpack_points = self.backpack.apacity
        self.items_max = 30 + self.backpack_points
        if self.armor:
            self.armor_points = self.armor.strength
        self.lives_max = 10
        self.lives = self.lives_max
        self.damage = 1
        self.sound_damage = Sound(s.S_DAMAGE["kick"])

    @classmethod
    def cheater(cls, xy: Tuple[int, int], game) -> "Hero":
        """ делает читера (герой с сверх способностями)
        @param xy: координаты читера на карте/map
        @param game: ссылка на игру
        @return: герой
        """
        cheater = cls(name="cheater", image="cheater.png", xy=xy, game=game)
        cheater.items = [Digle(), Uzi(), Kalashnikov(), HeavyCartridge(), Fraction(),
                         LittleCartridge(), Awp(), Mastif(), Knife(), Armor1(), Medikit(),
                         Cotton(), Backpack1()]
        cheater.item_in_hands = Digle()
        cheater.items_max = 1000
        cheater.actions = 10000
        return cheater

    def move(self, pressed_key: int) -> None:
        """ Передвижение героя по карте """
        # получаем направление движения
        direction = f.get_direction(pressed_key)
        if not direction:
            return
        self.action_direction = direction

        # если стенка есть двигаем героя в сторону стенки до остановки
        if self.my_cell().has_wall(direction):
            self._move_to_wall(direction)
            return
        # если стенки нет передвигаем героя на новую клетку
        self._move_to_cell(direction)

    def _move_to_wall(self, direction: str) -> None:
        """ герой двигается в сторону стенки"""
        self.action_type = "move_to_wall"
        self.action_direction = direction
        self.action_start_time = datetime.now()
        self.action_silent = False

    def _move_to_cell(self, direction: str) -> None:
        """ герой двигается в сторону клетки"""
        # найдём клетку в направлении движения
        xy = dict(
            up=(self.xy[0], self.xy[1] - 1),
            down=(self.xy[0], self.xy[1] + 1),
            right=(self.xy[0] + 1, self.xy[1]),
            left=(self.xy[0] - 1, self.xy[1]),
        ).get(direction, self.xy)

        # найдём клетку в направлении движения
        # xy = self.xy
        # if direction == "up":
        #     xy = (self.xy[0], self.xy[1] - 1)
        # elif direction == "down":
        #     xy = (self.xy[0], self.xy[1] + 1)
        # elif direction == "right":
        #     xy = (self.xy[0] + 1, self.xy[1])
        # elif direction == "left":
        #     xy = (self.xy[0] - 1, self.xy[1])

        cell_to = self.game.map.get_cell(xy)
        if not cell_to:
            return
        # инкремент счётчика действий
        self.actions -= 1
        self.move_to_cell(cell_to)
        self.key_pressed = True
        self.action_silent = True  # TODO

        self.action_type = "move_to_cell"
        self.action_direction = direction
        self.action_start_time = datetime.now()
        self.action_silent = False

    def add_carts_to_backpack(self, item: "Cartridge") -> None:
        """ добавляет патроны к рюкзак """
        # патроны того же типа у героя
        slots_with_cartridges = [o for o in self.items if o.kind == item.kind]
        for slot in slots_with_cartridges:
            # если слот с патронами переполнен, ещем следующий свободный слот
            if slot.count >= slot.count_max:
                continue
            # если слот с патронами не переполнен, кладём патроны в рюкзак
            slot.count += item.count
            break
        else:
            if len(self.items) < self.items_max:  # если рюкзак не полный
                self.items.append(item)  # кладём патроны в рюкзак

    def pickup_item(self) -> None:
        """ герой поднемает вещь на карте """
        cell = self.my_cell()
        # выходим если вещей нет на клетке
        if not cell.items:
            return
        # выходим если рюкзак полный
        if len(self.items) >= self.items_max:
            return
        # поднимает вещь с карты и ложим вещь в рюкзак
        Sound(s.S_PICK_UP).play()
        item_picked = cell.pop_item()
        self.actions -= 1
        # если это патроны
        if item_picked.kind_0 == "cart":
            self.add_carts_to_backpack(item_picked)
        # если это не патроны
        else:
            self.items.append(item_picked)

    def drop_down_item(self) -> None:
        """ выбрасываем вещь из рук на карту """
        # выходим если вещи нет в руках
        if not self.item_in_hands:
            return
        # выбрасываем вещь
        Sound(s.S_DROP_DOWN).play()
        item = self.item_in_hands
        cell = self.my_cell()
        cell.append_item(item)
        self.item_in_hands = None

    def wear(self) -> None:
        """ Одевает броню или рюкзак """
        if not self.item_in_hands:
            return
        if self.item_in_hands.kind_0 == "armor":
            if not self.armor:
                self.armor = self.item_in_hands
                self.item_in_hands = None
            else:
                armor = self.armor
                self.armor = self.item_in_hands
                self.items.append(armor)
                self.item_in_hands = None

        elif self.item_in_hands.kind_0 == "backpack":
            if not self.backpack:
                self.backpack = self.item_in_hands
                self.item_in_hands = None
                self.items_max += self.backpack.capacity
            else:
                backpack = self.backpack
                self.items_max -= backpack.capacity
                self.backpack = self.item_in_hands
                self.items_max += backpack.capacity
                self.items.append(backpack)
                self.item_in_hands = None

    def use(self) -> None:
        """ используем вещь в руках """
        item = self.item_in_hands
        if not item:
            return
        if item.kind == "Medikit":
            self.lives += item.heal
            self.lives = min([self.lives, self.lives_max])
            self.item_in_hands = None
            self.game.items.remove(item)
            return
        if item.kind == "Cotton":
            if self.armor:
                self.armor.strength += item.heal
                self.game.items.remove(item)
                self.item_in_hands = None

    def attack(self, pressed_key) -> None:
        """ атакует персонажа на соседней клетке """
        direction = f.get_direction(pressed_key)
        map_ = self.game.map
        my_cell = self.my_cell()
        weapon = self.item_in_hands
        self.actions -= 1

        # рукапашный бой, атакуем свою клетку
        if not weapon or weapon.kind_0 not in ["gun", "steelweapon"]:
            self.sound_damage.play()
            cell_attacked = self.my_cell()
            ch_attacked = cell_attacked.get_character_without(self)
            if ch_attacked:
                ch_attacked.do_damage(1)
            return

        # огнестрел
        if weapon.kind_0 == "gun":
            bullets = self._bullets_from_backpack(weapon)
            if not bullets:
                # TODO sound
                return
            # выстрелы
            for bullet in range(bullets):
                weapon.sound_use.play()
                # вероятность промаха
                if random.uniform(0, 1) > weapon.hit_probability:
                    # TODO sound
                    continue
                # атакуемые клетки
                cells_attacked = map_.get_direction_cells(my_cell, direction, weapon.range)
                # пуля попадает в первого попавшевося персонажа или в стенку
                for cell_i in cells_attacked:
                    ch_attacked = cell_i.get_character()
                    if ch_attacked:
                        ch_attacked.do_damage(weapon.damage)
                    if direction in cell_i.walls:
                        # cell_i.rikoshet.play()  # TODO sound
                        break
            return

        # холодное оружие
        if weapon.kind_0 == "steelweapon":
            cell_attacked = map_.get_direction_cell(my_cell, direction)
            ch_attacked = cell_attacked.get_character()
            if ch_attacked:
                # оружие теряет прочность
                weapon.reduce_strength()
                if weapon.strength > 0:
                    weapon.sound_use.play()
                    ch_attacked.do_damage(weapon.damage)
                else:
                    weapon.sound_breaking.play()
                    self.item_in_hands = None




            return


    def _bullets_from_backpack(self, weapon: "Guns") -> int:
        """ return патроны из рюкзака для данного типа оружия """
        bullets = 0
        for item in self.items:
            if item.kind != weapon.cartridge_kind:
                continue
            # уменьшаем количество птронов в слоте рюкзака на количество выстрелов
            bullets = weapon.fire_speed
            if item.count < weapon.fire_speed:
                bullets = item.count
            item.count -= bullets
            if item.count <= 0:
                self.items.remove(item)
        return bullets
