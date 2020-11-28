""" Персонаж герой """

import os
import random
from datetime import datetime
from typing import Optional, Tuple

import pygame
from pygame.mixer import Sound

import settings as s
from character import Character
from items import Digle, Uzi, Kalashnikov, LittleCartridge, HeavyCartridge, Fraction, Mastif, \
    Awp, Medikit, Knife, Armor1, Cotton, Backpack1

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
        self.items_max = 3 + self.backpack_points
        if self.armor:
            self.armor_points = self.armor.strength
        self.lives = 10 + self.armor_points

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
        direction: Optional[str] = {
            pygame.K_UP: "up",
            pygame.K_DOWN: "down",
            pygame.K_RIGHT: "right",
            pygame.K_LEFT: "left",
        }.get(pressed_key)
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
        xy = self.xy
        if direction == "up":
            xy = (self.xy[0], self.xy[1] - 1)
        elif direction == "down":
            xy = (self.xy[0], self.xy[1] + 1)
        elif direction == "right":
            xy = (self.xy[0] + 1, self.xy[1])
        elif direction == "left":
            xy = (self.xy[0] - 1, self.xy[1])
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
        if self.item_in_hands:
            if self.item_in_hands.kind == "medikit":
                self.lives += self.item_in_hands.heal
                self.item_in_hands = None
                if self.lives >= 10:
                    self.lives = 10
            if self.item_in_hands.kind == "Cotton":
                if self.armor:
                    self.armor.strength += self.item_in_hands.heal
                    self.item_in_hands = None

    def attack(self, pressed_key) -> None:
        """ атакует персонажа на соседней клетке """
        map_ = self.game.map
        xy = self.xy
        wall = None

        # рукапашный бой
        if self.item_in_hands is None:
            # находим атакуемую клетку
            if pressed_key == pygame.K_UP:
                cell_attacked = map_.get_cell((xy[0], xy[1] - 1))
            elif pressed_key == pygame.K_DOWN:
                cell_attacked = map_.get_cell((xy[0], xy[1] + 1))
            elif pressed_key == pygame.K_LEFT:
                cell_attacked = map_.get_cell((xy[0] - 1, xy[1]))
            elif pressed_key == pygame.K_RIGHT:
                cell_attacked = map_.get_cell((xy[0] + 1, xy[1]))
            else:
                cell_attacked = None

            # отнимает жизьни у атакуюмого персонажа
            if cell_attacked.characters:
                Sound(s.SOUNDS["kick"]).play()
                # получает последнего персонажа в этой клетке
                ch_attacked = cell_attacked.characters[-1]
                ch_attacked.lives -= 1
                self.actions -= 1
                if ch_attacked.lives <= 0:
                    ch_attacked.death()

        # gun
        elif self.item_in_hands:
            if self.item_in_hands.kind_0 == "gun":
                for item in self.items:
                    # ищет патроны нужного типа в рюкзаке
                    if item.kind == self.item_in_hands.cartridge_kind:
                        item.count -= self.item_in_hands.fire_speed
                        if item.count <= 0:
                            self.items.remove(item)

                        # находим атакуемые клетки на линии поражения range и дабовляет их в лист
                        cells_attacked = []
                        for i in range(self.item_in_hands.range + 1):
                            if pressed_key == pygame.K_UP:
                                cells_attacked.append(map_.get_cell((xy[0], xy[1] - i)))
                                wall = "down"
                            elif pressed_key == pygame.K_DOWN:
                                cells_attacked.append(map_.get_cell((xy[0], xy[1] + i)))
                                wall = "up"
                            elif pressed_key == pygame.K_LEFT:
                                cells_attacked.append(map_.get_cell((xy[0] - i, xy[1])))
                                wall = "right"
                            elif pressed_key == pygame.K_RIGHT:
                                cells_attacked.append(map_.get_cell((xy[0] + i, xy[1])))
                                wall = "left"
                            if cells_attacked[-1] is None:
                                cells_attacked.remove(cells_attacked[-1])
                                break
                        # никого не стреляет в собственной клетке
                        cells_attacked.remove(cells_attacked[0])
                        self.item_in_hands.sound_use.play()

                        # летит пуля
                        # попадает в первого попавшевося персонажа или в стенку на линии поражения
                        is_bullet_flies = True
                        for cell_i in cells_attacked:
                            if not is_bullet_flies:
                                break
                            if wall in cell_i.walls:  # todo исправить
                                cell_i.rikoshet.play()
                                break

                            # time.sleep(1)  # todo sound pause in every cell, like song distance
                            for _ in range(self.item_in_hands.fire_speed):
                                for _ in range(self.item_in_hands.range):

                                    # self.item_in_hands.sound_use.play()
                                    # self.item_in_hands.sound_use.play()
                                    # sound
                                    # Sound(self.item_in_hands.sound_use).play()
                                    # проверяет есть ли на пути стенки

                                    # вероятность попадания 50%
                                    if random.randrange(100) < 70:
                                        # if wall in cell_i.walls:
                                        #     cell_i.rikoshet.play()
                                        #     break
                                        continue

                                    # проверяет есть ли на клетки персонаж
                                    if cell_i and cell_i.characters:
                                        # получает последнего персонажа в этой клетке
                                        ch_attacked = cell_i.characters[-1]
                                        # наносм персонажу определённый урон
                                        ch_attacked.lives -= self.item_in_hands.damage
                                        is_bullet_flies = False
                                        # если мы убили персонажа то меняет active_id
                                        if ch_attacked.lives <= 0:
                                            ch_attacked.death()
                            # никого, промах
                            if not cells_attacked:
                                rikoshet = Sound(
                                    os.path.join(s.SOUNDS_DIR, "rikoshet.wav"))
                                rikoshet.play()

                            self.actions -= 1

            #
            # elif self.item_in_hands.kind_0 == "grenade":  # todo grenade
            #     pass
            elif self.item_in_hands.kind_0 == "steelweapon":
                cell_attacked = None  # атакуемая клетка
                if pressed_key == pygame.K_UP:
                    cell_attacked = map_.get_cell((xy[0], xy[1] - 1))
                elif pressed_key == pygame.K_DOWN:
                    cell_attacked = map_.get_cell((xy[0], xy[1] + 1))
                elif pressed_key == pygame.K_LEFT:
                    cell_attacked = map_.get_cell((xy[0] - 1, xy[1]))
                elif pressed_key == pygame.K_RIGHT:
                    cell_attacked = map_.get_cell((xy[0] + 1, xy[1]))

                # отнимает жизьни у атакуюмого персонажа
                if cell_attacked.characters:
                    # получает последнего персонажа в этой клетке
                    ch_attacked = cell_attacked.characters[-1]
                    ch_attacked.lives -= self.item_in_hands.damage
                    if ch_attacked.lives <= 0:
                        ch_attacked.death()
                    if random.randrange(100) < 50:
                        self.item_in_hands.strength -= 1
                    else:
                        self.item_in_hands.strength -= 2
                    if self.item_in_hands.strength <= 0:
                        self.item_in_hands = None
                    self.actions -= 1
                    if ch_attacked.lives == 0:
                        ch_attacked.death()
