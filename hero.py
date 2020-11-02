""" Персонажы """

import os
import random
from typing import Tuple, List

import pygame
from pygame import Rect

import constants as c
from character import Character
from Items import Digle, Uzi, Kalashnikov, LittleCartridge, HeavyCartridge, Fraction, Mastif, Awp, \
    Medikit, Knife, Armor_level_1, Cotton, Backpack_level_3


class Hero(Character):
    """ Герой """

    def __init__(self, name, image, cell_xy, game):
        super().__init__(name, image, cell_xy, game)
        self.type = "hero"
        self.items = []  # колличество вещей
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
    def cheater(cls, game):
        """ делает читера """
        cheater = cls(name="cheater", image="cheater.png", cell_xy=(1, 1), game=game)
        cheater.items = [Digle(), Uzi(), Kalashnikov(), HeavyCartridge(), Fraction(),
                         LittleCartridge(), Awp(), Mastif(), Knife(), Armor_level_1(), Medikit(),
                         Cotton(), Backpack_level_3()]
        cheater.item_in_hands = Digle()
        cheater.items_max = 1000
        cheater.actions = 10000

    def move(self, pressed_key) -> None:
        """ Передвижение героя по карте """
        map_ = self.game.map
        # найдём ячейку в которой находится персонаж
        cell = map_.get_cell_by_xy(tuple(self.cell_xy))

        # герой переходит на другую клетку
        is_success = False

        # если стенки нет двигает персонажа
        if pressed_key == pygame.K_UP:
            if 't' not in cell.walls:
                self.cell_xy[1] -= 1
                is_success = True
        elif pressed_key == pygame.K_DOWN:
            if 'b' not in cell.walls:
                self.cell_xy[1] += 1
                is_success = True
        elif pressed_key == pygame.K_RIGHT:
            if 'r' not in cell.walls:
                self.cell_xy[0] += 1
                is_success = True
        elif pressed_key == pygame.K_LEFT:
            if 'l' not in cell.walls:
                self.cell_xy[0] -= 1
                is_success = True

        # инкремент счётчика действий или звук столкновения персонажа со стеной
        if pressed_key in [pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT]:
            # инкремент счётчика действий
            if is_success is True:
                self.rect = self._get_rect()
                self.actions -= 1
                self.key_pressed = True

                # меняет положение героя на карте
                try:
                    cell.characters.remove(self)
                except Exception:
                    print()
                for cell_ in map_.cells:
                    if cell_.xy == tuple(self.cell_xy):
                        cell_.characters.append(self)

            # звук столкновения персонажа со стеной
            else:
                # pygame.mixer.Sound(c.SOUND_PUNCH_TO_WALL).play()  # todo repair sounds
                pass
        # print()

    def pick_up_item(self) -> None:
        """ герой поднемает вещь на карте """
        map_ = self.game.map
        is_success = False
        for cell in map_.cells:
            if cell.xy == tuple(self.cell_xy):  # если герой стоит на этой ячейке
                if cell.items:  # если вещь есть на ячейке
                    item_on_map = cell.items.pop()  # поднимает вещь с карты

                    # если это патроны
                    if item_on_map.kind_0 == 'cart':
                        # патроны того же типа в рюкзаке
                        carts_the_same = [i for i in self.items if i.kind == item_on_map.kind]
                        if carts_the_same:  # если в рюкзаке патроны, то добавляет к существуещим
                            for cart in carts_the_same:
                                if cart.count >= cart.count_max:  # если слот с патронами переполнен
                                    continue
                                else:  # если слот с патронами не переполнен
                                    cart.count += item_on_map.count  # кладём вещь в рюкзак
                                    break
                            else:
                                if len(self.items) < self.items_max:  # если рюкзак не полный
                                    self.items.append(item_on_map)  # кладём патроны в рюкзак
                            is_success = True

                        else:  # если в рюкзаке патронав нет
                            if len(self.items) < self.items_max:  # если рюкзак не полный
                                self.items.append(item_on_map)  # кладём вещь в рюкзак
                                is_success = True

                    # если это не патроны
                    else:
                        if len(self.items) < self.items_max:  # если рюкзак не полный
                            self.items.append(item_on_map)  # кладём в рюкзак
                            is_success = True

                    # если рюкзак полный, вернём вещь на карту
                    if len(self.items) >= self.items_max:
                        cell.items.append(item_on_map)

        if is_success is True:
            self.actions -= 1

    def drop_down_item(self) -> None:
        """ выбрасывает вещь из рук на карту """
        map_ = self.game.map
        if self.item_in_hands is None:
            return
        else:
            cell = map_.get_cell_by_xy(tuple(self.cell_xy))
            cell.items.append(self.item_in_hands)
            self.item_in_hands = None

    def wear(self) -> None:
        """ Одевает броню или рюкзак """
        if self.item_in_hands:
            if self.item_in_hands.kind_0 == "armor":
                if not self.armor:
                    self.armor = self.item_in_hands
                    self.item_in_hands = None
                else:
                    armor = self.armor
                    self.armor = self.item_in_hands
                    self.items.append(armor)
                    self.item_in_hands = None

            if self.item_in_hands.kind_0 == "backpack":
                if not self.backpack:
                    self.backpack = self.item_in_hands
                    self.item_in_hands = None
                    self.items_max += self.backpack.apacity
                else:
                    backpack = self.backpack
                    self.items_max -= backpack.apacity
                    self.backpack = self.item_in_hands
                    self.items_max += backpack.apacity
                    self.items.append(backpack)
                    self.item_in_hands = None

    def use(self):
        print(self.items_max)
        if self.item_in_hands:
            if self.item_in_hands.kind == 'medikit':
                self.lives += self.item_in_hands.heal
                self.item_in_hands = None
                if self.lives >= 10:
                    self.lives = 10
            if self.item_in_hands.kind == 'cotton':
                if self.armor:
                    self.armor.strength += self.item_in_hands.heal
                    self.item_in_hands = None

    def attack(self, pressed_key) -> None:
        """ атакует персонажа на соседней клетке """
        map_ = self.game.map
        cell_xy = self.cell_xy
        wall = None

        # рукапашный бой
        if self.item_in_hands is None:
            # находим атакуемую клетку
            cell_attacked = None  # атакуемая клетка
            if pressed_key == pygame.K_UP:
                cell_attacked = map_.get_cell_by_xy((cell_xy[0], cell_xy[1] - 1))
            elif pressed_key == pygame.K_DOWN:
                cell_attacked = map_.get_cell_by_xy((cell_xy[0], cell_xy[1] + 1))
            elif pressed_key == pygame.K_LEFT:
                cell_attacked = map_.get_cell_by_xy((cell_xy[0] - 1, cell_xy[1]))
            elif pressed_key == pygame.K_RIGHT:
                cell_attacked = map_.get_cell_by_xy((cell_xy[0] + 1, cell_xy[1]))

            # отнимает жизьни у атакуюмого персонажа
            if cell_attacked.characters:
                # получает последнего персонажа в этой клетке
                ch_attacked = cell_attacked.characters[-1]
                ch_attacked.lives -= 1
                self.actions -= 1
                if ch_attacked.lives == 0:
                    ch_attacked.death()

        # gun
        elif self.item_in_hands:
            if self.item_in_hands.kind_0 == 'gun':
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
                                cells_attacked.append(map_.get_cell_by_xy((cell_xy[0], cell_xy[1] - i)))
                                wall = 'b'
                            elif pressed_key == pygame.K_DOWN:
                                cells_attacked.append(map_.get_cell_by_xy((cell_xy[0], cell_xy[1] + i)))
                                wall = 't'
                            elif pressed_key == pygame.K_LEFT:
                                cells_attacked.append(map_.get_cell_by_xy((cell_xy[0] - i, cell_xy[1])))
                                wall = 'r'
                            elif pressed_key == pygame.K_RIGHT:
                                cells_attacked.append(map_.get_cell_by_xy((cell_xy[0] + i, cell_xy[1])))
                                wall = 'l'
                            if cells_attacked[-1] is None:
                                cells_attacked.remove(cells_attacked[-1])
                                break
                        # никого не стреляет в собственной клетке
                        cells_attacked.remove(cells_attacked[0])

                        if self.item_in_hands.sound_shot.get_num_channels() >= 1:
                            self.item_in_hands.sound_shot.stop()
                        self.item_in_hands.sound_shot.play()

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

                                    # self.item_in_hands.sound_shot.play()
                                    # self.item_in_hands.sound_shot.play()
                                    # sound
                                    # pygame.mixer.Sound(self.item_in_hands.sound_shot).play()
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
                                rikoshet = pygame.mixer.Sound(
                                    os.path.join(c.SOUNDS_DIR, 'rikoshet.wav'))
                                rikoshet.play()

                            self.actions -= 1

            #
            # elif self.item_in_hands.kind_0 == 'grenade':  # todo
            #     pass
            elif self.item_in_hands.kind_0 == 'steelweapon':  # todo
                cell_attacked = None  # атакуемая клетка
                if pressed_key == pygame.K_UP:
                    cell_attacked = map_.get_cell_by_xy((cell_xy[0], cell_xy[1] - 1))
                elif pressed_key == pygame.K_DOWN:
                    cell_attacked = map_.get_cell_by_xy((cell_xy[0], cell_xy[1] + 1))
                elif pressed_key == pygame.K_LEFT:
                    cell_attacked = map_.get_cell_by_xy((cell_xy[0] - 1, cell_xy[1]))
                elif pressed_key == pygame.K_RIGHT:
                    cell_attacked = map_.get_cell_by_xy((cell_xy[0] + 1, cell_xy[1]))

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
