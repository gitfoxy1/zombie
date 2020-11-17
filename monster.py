""" Персонажы """

import random
from time import sleep
from typing import List, Optional, Set, Tuple, Union

import pygame

import constants as c
from character import Character
from map import Cell

TRoute = List[List[Cell]]


class Monster(Character):
    """ Монстр """
    route: List[Cell] = list()  # маршрут монстпа к герою

    # noinspection PyUnresolvedReferences
    def __init__(self, name: str, image: str, xy: Tuple[int, int], actions_max: int, lives: int,
                 damage: int, iq: int, game: "Game"):
        """ Монстр
        @param name: имя монстра
        @param image: картинка
        @param xy: координаты клетки на карте
        @param actions_max: максимальное количество действий
        @param lives: количество здоровья
        @param damage: урон за одно действие
        @param game: ссылка на объект game
        """
        super().__init__(name, image, xy, game)
        self.type = "monster"
        self.actions_max = actions_max  # максимально количество действий монстра за один ход игры
        self.actions = 0  # количество действий на данный момент
        self.lives = lives
        self.damage = damage
        self.iq = iq

    # noinspection PyUnresolvedReferences
    @classmethod
    def little(cls, name: str, xy: Tuple[int, int], game: "Game"):
        """ создадим маленького монстра """
        monster = cls(name=name,
                      image="little_monster.png",
                      xy=xy,
                      actions_max=3,
                      lives=1,
                      damage=1,
                      iq=5,
                      game=game)
        return monster

    # noinspection PyUnresolvedReferences
    @classmethod
    def big(cls, name: str, xy: Tuple[int, int], game: "Game"):
        """ создадим большого монстра """
        monster = cls(name=name,
                      image="big_monster.png",
                      xy=xy,
                      actions_max=3,
                      lives=3,
                      damage=1,
                      iq=7,
                      game=game)
        return monster

    @classmethod
    def boss_1(cls, name: str, xy: Tuple[int, int], game: "Game"):
        """ создадим большого монстра """
        monster = cls(name=name,
                      image="monster_boss_1.png",
                      xy=xy,
                      actions_max=3,
                      lives=10,
                      damage=1,
                      iq=10,
                      game=game)
        return monster

    @classmethod
    def fast(cls, name: str, xy: Tuple[int, int], game: "Game"):
        """ создадим большого монстра """
        monster = cls(name=name,
                      image="fast_monster.png",
                      xy=xy,
                      actions_max=6,
                      lives=2,
                      damage=1,
                      iq=6,
                      game=game)
        return monster

    @classmethod
    def eye(cls, name: str, xy: Tuple[int, int], game: "Game"):
        """ создадим большого монстра """
        monster = cls(name=name,
                      image="eye.png",
                      xy=xy,
                      actions_max=3,
                      lives=2,
                      damage=3,
                      iq=8,
                      game=game)
        return monster

    @classmethod
    def boss_2(cls, name: str, xy: Tuple[int, int], game: "Game"):
        """ создадим большого монстра """
        monster = cls(name=name,
                      image="monster_boss_2.png",
                      xy=xy,
                      actions_max=6,
                      lives=10,
                      damage=1,
                      iq=11,
                      game=game)
        return monster

    @classmethod
    def shooting(cls, name: str, xy: Tuple[int, int], game: "Game"):
        """ создадим большого монстра """
        monster = cls(name=name,
                      image="shoting_monster.png",
                      xy=xy,
                      actions_max=3,
                      lives=2,
                      damage=2,
                      iq=7,
                      game=game)
        return monster

    @classmethod
    def smart(cls, name: str, xy: Tuple[int, int], game: "Game"):
        """ создадим большого монстра """
        monster = cls(name=name,
                      image="smart_monster.png",
                      xy=xy,
                      actions_max=3,
                      lives=2,
                      damage=2,
                      iq=15,
                      game=game)
        return monster


    def route_to_hero(self, iq_level: int) -> List[Cell]:
        """ монстр ищет маршрут к герою """
        # найдём клетку в которой находится персонаж
        cell = self.get_cell()
        # получаем самый короткий путь до героя
        routes = list()
        for _ in range(iq_level):
            routes_i = self.random_routes_to_hero(cell)
            routes_i = sorted(routes_i, key=lambda i: len(i))
            route = routes_i[0]
            routes.append(route)
        routes = sorted(routes, key=lambda i: len(i))
        route = routes[0]
        return route

    def random_routes_to_hero(self, cell: Cell, cells_checked: Set[Cell] = None,
                              routes: TRoute = None) -> Union[TRoute, Cell]:
        """ ищем путь от монстра до героя
        - проверяем есть ли на клетке герой, если герой есть, то возвращаем клетки
            через которые прошли
        - если героя нет на клетке, то мы перебираем все соседние клетки
        @param cell: активная клетка в которой исчем путь (следующую клетку)
        @param cells_checked: клетки в которых уже искали в предыдущих рекурсииях
        @param routes: пути от героя к монстру
        """
        if not cells_checked:
            cells_checked = set()
        if not routes:
            routes = list()

        #  проверяем есть ли на клетке герой, если герой есть, то останавливаем рекурсию
        hero_in_cell = [o for o in cell.characters if o.type == "hero"]
        if hero_in_cell:
            return [[cell]]

        # если героя нет на клетке, то мы перебираем все соседние клетки
        cells_checked.add(cell)
        directions = c.WALLS.copy()  # все возможные направления
        directions.difference_update(cell.walls)  # возможные направления без стен
        directions = sorted(directions)
        random.shuffle(directions)
        cell_next = None
        for direction in directions:
            # возможное направление клетка сверху
            if direction == "t":
                xy = (cell.xy[0], cell.xy[1] - 1)
                cell_next = self.game.map.get_cell(xy)
            # возможное направление клетка снизу
            elif direction == "b":
                xy = (cell.xy[0], cell.xy[1] + 1)
                cell_next = self.game.map.get_cell(xy)
            # возможное направление клетка слева
            elif direction == "l":
                xy = (cell.xy[0] - 1, cell.xy[1])
                cell_next = self.game.map.get_cell(xy)
            # возможное направление клетка справа
            elif direction == "r":
                xy = (cell.xy[0] + 1, cell.xy[1])
                cell_next = self.game.map.get_cell(xy)
            # пропускает клетку в которой уже были
            if cell_next in cells_checked:
                continue
            # # draw  # todo debug
            # pygame.draw.line(self.game.screen, c.BLUE, cell.center(), cell_next.center(), 10)
            # pygame.display.update()
            # sleep(0.01)

            # рекурсивный поиск героя в следующей клетке
            route_to_hero = self.random_routes_to_hero(cell_next, cells_checked, [])
            # если нашли героя, добавим новый туть в список маршрутов
            routes.extend(route_to_hero)

        # если список маршрутов/routes не пустой, добавим клетку во все пути
        for route in routes:
            route.insert(0, cell)
        return routes

    def move(self) -> None:
        """ Передвижение монстра по карте """
        is_hero = False
        if not self.actions:
            return
        cell = self.game.map.get_cell(self.xy)
        for c in cell.characters:
            if c.type == 'hero':
                is_hero = True
        if is_hero:
            self.route = [cell, cell]
        else:
            # получаем самый короткий путь до героя, в зависимости от интелекта
            route = self.route_to_hero(iq_level=self.iq)
            if len(route) <= 2:
                self.route = route
                return
            # передвигаем монтра по маршруту
            route = route[1:]  # убирает из маршрута превую клетку (где стоит монстр)
            cell_to = route[0]
            self.move_to_cell(cell_to)
            self.actions -= 1
            self.route = route

    def attack(self) -> None:
        """ монстр атакует героя """
        if not self.actions:
            return
        # выходим если героя нет на соседней клетке
        if len(self.route) > 2:
            return
        # атака
        cell_attacked = self.route[1]
        hero = cell_attacked.get_hero()
        if hero:
            hero.lives -= self.damage
            if hero.lives <= 0:
                hero.death()
        self.actions -= 1
