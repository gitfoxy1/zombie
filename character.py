import pygame
import math
import os
from backpack import Backpack
import random
import time

import constants as c
from Items import Digle, Uzi, Kalashnikov, LittleCartridge, HeavyCartridge, Fraction, Mastif, Awp, Knife


class Character:
    """ Персонаж, класс-родитель для героя и монстра """
    def __init__(self, name, image, xy):
        self.type = None
        self.name = name  # имя персонажа
        self.xy = list(xy)  # координаты персонажа на карте
        self.scale = 0.9  # размер персонажа относительно ячейки карты
        self.w = int(c.CELL_W * self.scale)  # ширина персонажа по оси x
        self.h = self.w  # высота персонажа по оси y
        self.image = pygame.image.load(os.path.join(c.IMAGES_DIR, image))
        self.pic = pygame.transform.scale(self.image, (self.w, self.h))  # лицо
        self.rect = self.pic.get_rect()
        self.items = []
        self.lives = None
        self.item_in_hands = None  # вещь на руках

        self.actions_max = 3  # максимально количество действий героя за один ход игры
        self.actions = self.actions_max  # возможное количество действий на данный момент

    def draw(self, screen):
        """ Рисуем персонажа на карте """
        cell_x = c.CELL_W * self.xy[0]  # координаты ячкйки на экрана
        cell_y = c.CELL_W * self.xy[1]
        x = cell_x + c.CELL_W / 2 - self.w / 2  # координаты героя на экрана, центр героя в центре ячейки
        y = cell_y + c.CELL_W / 2 - self.h / 2
        pic = pygame.transform.scale(self.pic, (self.w, self.h))
        screen.blit(pic, (x, y))

    def move(self, event, map_):
        """ Передвижение персонажа по карте """
        # найдём ячейку в которой находится персонажа
        cell = map_.get_cell_by_xy(tuple(self.xy))
        # cell0 = [i for i in map_.cells if i.xy == tuple(self.xy)][0]  # найдём ячейку в которой находится герой

        # герой переходит на другую клетку
        is_success = False

        if event.key == pygame.K_UP:
            if 't' not in cell.walls:  # если стенки нет
                self.xy[1] -= 1  # двигаем персонажа
                is_success = True
        elif event.key == pygame.K_DOWN:
            if 'b' not in cell.walls:
                self.xy[1] += 1
                is_success = True
        elif event.key == pygame.K_RIGHT:
            if 'r' not in cell.walls:
                self.xy[0] += 1
                is_success = True
        elif event.key == pygame.K_LEFT:
            if 'l' not in cell.walls:
                self.xy[0] -= 1
                is_success = True

        # инкремент счётчика действий или звук столкновения персонажа со стеной
        if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT]:
            # инкремент счётчика действий
            if is_success is True:
                self.actions -= 1

                # меняет положение героя на карте
                cell.characters.remove(self)
                for cell_ in map_.cells:
                    if cell_.xy == tuple(self.xy):
                        cell_.characters.append(self)
            # звук столкновения персонажа со стеной
            else:
                # pygame.mixer.Sound(c.SOUND_PUNCH_TO_WALL).play()  # todo repair sounds
                pass

    def death(self, characters_all, cell_attacked):
        """ Персонаж умирает """
        characters_all.remove(self)
        cell_attacked.characters.remove(self)
        if self.items:
            for item in self.items:
                cell_attacked.items.append(item)


class Hero(Character):
    def __init__(self, name, image, xy):
        super().__init__(name, image, xy)
        self.type = 'hero'
        self.items = []  # колличество вещей
        self.items_max = 3
        self.lives = 1

    def pick_up_item(self, map_):
        """ герой поднемает вещь на карте """
        is_success = False

        for cell in map_.cells:
            if cell.xy == tuple(self.xy):  # если герой стоит на этой ячейке
                if cell.items:  # если вещь есть на ячейке
                    item_on_map = cell.items.pop()  # поднимаем вещь с карты

                    # если это патроны
                    if item_on_map.kind_0 == 'cart':
                        carts_the_same = [i for i in self.items if i.kind == item_on_map.kind]  # патроны того же типа в рюкзаке
                        if carts_the_same:  # если в рюкзаке патроны, то добавим к существуещим
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

    def drop_down_item(self, map_):
        """ выбрасываем вещь из рук на карту """
        if self.item_in_hands is None:
            return
        else:
            cell = map_.get_cell_by_xy(tuple(self.xy))
            cell.items.append(self.item_in_hands)
            self.item_in_hands = None

    def get_item_to_hands(self, backpack):
        """ берём вещь в руки из рюкзака """
        if self.item_in_hands:
            self.items.append(self.item_in_hands)
        self.item_in_hands = self.items.pop(backpack.active_items_id)

    def attack(self, event, map_, charecters) -> int:
        """ атакуем персонажа на соседней клетке """
        xy = self.xy
        self_active_id = charecters.index(self)
        wall = None

        if self.item_in_hands is None:
            # находим атакуемую клетку
            cell_attacked = None  # атакуемая клетка
            if event.key == pygame.K_UP:
                cell_attacked = map_.get_cell_by_xy((xy[0], xy[1] - 1))
            elif event.key == pygame.K_DOWN:
                cell_attacked = map_.get_cell_by_xy((xy[0], xy[1] + 1))
            elif event.key == pygame.K_LEFT:
                cell_attacked = map_.get_cell_by_xy((xy[0] - 1, xy[1]))
            elif event.key == pygame.K_RIGHT:
                cell_attacked = map_.get_cell_by_xy((xy[0] + 1, xy[1]))

            # отнимаем жизьни у атакуюмого персонажа
            if cell_attacked.characters:
                ch_attacked = cell_attacked.characters[-1]  # получаем последнего персонажа в этой клетке
                ch_attacked.lives -= 1
                self.actions -= 1
                if ch_attacked.lives == 0:
                    ch_attacked.death(charecters, cell_attacked)
                    self_active_id = charecters.index(self)

        if self.item_in_hands:
            if self.item_in_hands.kind_0 == 'gun':
                for item in self.items:
                    # ищем патроны нужного типа в рюкзаке
                    if item.kind == self.item_in_hands.cartridge_kind:
                        item.count -= self.item_in_hands.fire_speed
                        if item.count <= 0:
                            self.items.remove(item)

                        # находим атакуемые клетки на линии поражения range и дабовляем их в лист
                        cells_attacked = []
                        for i in range(self.item_in_hands.range + 1):
                            if event.key == pygame.K_UP:
                                cells_attacked.append(map_.get_cell_by_xy((xy[0], xy[1] - i)))
                                wall = 'b'
                            elif event.key == pygame.K_DOWN:
                                cells_attacked.append(map_.get_cell_by_xy((xy[0], xy[1] + i)))
                                wall = 't'
                            elif event.key == pygame.K_LEFT:
                                cells_attacked.append(map_.get_cell_by_xy((xy[0] - i, xy[1])))
                                wall = 'r'
                            elif event.key == pygame.K_RIGHT:
                                cells_attacked.append(map_.get_cell_by_xy((xy[0] + i, xy[1])))
                                wall = 'l'
                            if cells_attacked[-1] is None:
                                cells_attacked.remove(cells_attacked[-1])
                                break

                        cells_attacked.remove(cells_attacked[0])

                        if self.item_in_hands.sound_shot.get_num_channels() >= 1:
                            self.item_in_hands.sound_shot.stop()
                        self.item_in_hands.sound_shot.play()

                        # летит пуля
                        # попадаем в первого попавшевося персонажа или в стенку на линии поражения
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
                                    # проверяем есть ли на пути стенки

                                    # вероятность попадания 50%
                                    if random.randrange(100) < 70:
                                        # if wall in cell_i.walls:
                                        #     cell_i.rikoshet.play()
                                        #     break
                                        continue

                                    # проверяем есть ли на клетки персонаж
                                    if cell_i and cell_i.characters:
                                        ch_attacked = cell_i.characters[-1]  # получаем последнего персонажа в этой клетке
                                        ch_attacked.lives -= self.item_in_hands.damage  # наносм персонажу определённый урон
                                        is_bullet_flies = False
                                        # если мы убили персонажа то меняем active_id
                                        if ch_attacked.lives <= 0:
                                            ch_attacked.death(charecters, cell_i)
                                            self_active_id = charecters.index(self)



                            if not cells_attacked:
                                rikoshet = pygame.mixer.Sound(os.path.join(c.SOUNDS_DIR, 'rikoshet.wav'))
                                rikoshet.play()

                            self.actions -= 1

        #
        # elif self.item_in_hands.kind_0 == 'grenade':  # todo
        #     pass
            elif self.item_in_hands.kind_0 == 'steelweapon':  # todo
                cell_attacked = None  # атакуемая клетка
                if event.key == pygame.K_UP:
                    cell_attacked = map_.get_cell_by_xy((xy[0], xy[1] - 1))
                elif event.key == pygame.K_DOWN:
                    cell_attacked = map_.get_cell_by_xy((xy[0], xy[1] + 1))
                elif event.key == pygame.K_LEFT:
                    cell_attacked = map_.get_cell_by_xy((xy[0] - 1, xy[1]))
                elif event.key == pygame.K_RIGHT:
                    cell_attacked = map_.get_cell_by_xy((xy[0] + 1, xy[1]))

                # отнимаем жизьни у атакуюмого персонажа
                if cell_attacked.characters:
                    ch_attacked = cell_attacked.characters[-1]  # получаем последнего персонажа в этой клетке
                    ch_attacked.lives -= self.item_in_hands.damage
                    if ch_attacked.lives <= 0:
                        ch_attacked.death(charecters, cell_attacked)
                        self_active_id = charecters.index(self)
                    if random.randrange(100) < 50:
                        self.item_in_hands.strength -= 1
                    else:
                        self.item_in_hands.strength -= 2
                    if self.item_in_hands.strength <= 0:
                        self.item_in_hands = None
                    self.actions -= 1
                    if ch_attacked.lives == 0:
                        ch_attacked.death(charecters, cell_attacked)
                        self_active_id = charecters.index(self)



        # рукапашный бой


        return self_active_id


class Monster(Character):
    def __init__(self, name, image, xy, actions, lives):
        super().__init__(name, image, xy)
        self.type = 'monster'
        self.actions_max = actions  # максимально количество действий монстра за один ход игры
        self.actions = self.actions_max  # возможное количество действий на данный момент
        self.lives = lives


class Cheater(Hero):
    def __init__(self, name, image, xy):
        super().__init__(name, image, xy)
        self.items = [Digle(), Uzi(), Kalashnikov(), HeavyCartridge(), Fraction(), LittleCartridge(), Awp(), Mastif(), Knife()]
        self.item_in_hands = Digle()
        self.items_max = 1000
        self.actions = 10000
