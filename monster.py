""" Персонажы """

from time import sleep
from typing import List, Optional, Set

import pygame

import constants as c
from character import Character
from map import Cell


# class Point(NamedTuple):
#     """ хоординаты на карте """
#     x: int
#     y: int


class Monster(Character):
    """ Монстр """
    route1: Optional[List[Cell]] = None  # маршрут снаружи дома
    route2: Optional[List[Cell]] = None  # маршрут внутри дома

    # noinspection PyUnresolvedReferences
    def __init__(self, name: str, image: str, xy: List[int], actions_max: int, lives: int,
                 damage: int, game: "Game"):
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
        # self.route1 = self.route_to_hero()  # todo
        # self.route2 = self.route_to_hero()

    # noinspection PyUnresolvedReferences
    @classmethod
    def little(cls, name: str, xy: List[int], game: "Game"):
        """ создадим маленького монстра """
        monster = cls(name=name,
                      image="little_monster.png",
                      xy=xy,
                      actions_max=2,
                      lives=1,
                      damage=1,
                      game=game)
        return monster

    # noinspection PyUnresolvedReferences
    @classmethod
    def big(cls, name: str, xy: List[int], game: "Game"):
        """ создадим большого монстра """
        monster = cls(name=name,
                      image="big_monster.png",
                      xy=xy,
                      actions_max=2,
                      lives=3,
                      damage=1,
                      game=game)
        return monster

    # @staticmethod 3 todo удалить
    # def choose_route1() -> Tuple[Tuple[int, int]]:
    #     """ выбирает маршрут для монстра """
    #     route = [Point(1, 4), Point(2, 4), Point(3, 5)]
    #     for point in route:
    #         print(point.x)
    #         print(point.y)
    #     print(route[0].y)
    #
    #     firsts_routes = [(1, 4), (2, 4)]
    #     for i in firsts_routes:
    #         print(i[0])
    #         print(i[1])
    #     print(firsts_routes[0][1])
    #
    #     firsts_route = random.choice(firsts_routes)
    #     return firsts_route

    def route_to_hero(self, cell: Cell, cells_previous: Set[Cell]) -> List[Cell]:
        """ ищем путь от монстра до героя
        - проверяем есть ли на клетке герой, если герой есть, то возвращаем клетки
            через которые прошли
        - если героя нет на клетке, то мы перебираем все соседние клетки
        @param cell: активная клетка в которой исчем путь (следующую клетку)
        @param cells_previous: клетки в которых уже искали в предыдущих рекурсииях
        """
        #  проверяем есть ли на клетке герой, если герой есть, то останавливаем рекурсию
        cell_hero = None
        for o in cell.characters:
            if o.type == "hero":
                return [cell]

        # если героя нет на клетке, то мы перебираем все соседние клетки
        cells_previous.add(cell)
        direction_variants = {"t", "b", "l", "r"}
        directions_next = direction_variants.difference(cell.walls)
        cell_next = None
        for direction_i in directions_next:
            # клетка сверху
            if direction_i == "t":
                x = cell.xy[0]
                y = cell.xy[1] - 1
                cell_next = self.game.map.get_cell([x, y])
            # клетка снизу
            elif direction_i == "b":
                x = cell.xy[0]
                y = cell.xy[1] + 1
                cell_next = self.game.map.get_cell([x, y])
            # клетка слева
            elif direction_i == "l":
                x = cell.xy[0] - 1
                y = cell.xy[1]
                cell_next = self.game.map.get_cell([x, y])
            # клетка справа
            elif direction_i == "r":
                x = cell.xy[0] + 1
                y = cell.xy[1]
                cell_next = self.game.map.get_cell([x, y])
            # пропускает клетку в которой уже были
            if cell_next in cells_previous:
                continue

            # print(cell, cell_next, cells_previous)

            x_tl = cell.xy[0] * cell.w
            y_tl = cell.xy[1] * cell.h
            point1 = (x_tl + cell.w / 2,
                      y_tl + cell.h / 2)
            point2 = (cell_next.xy[0] * cell_next.w + cell_next.w / 2,
                      cell_next.xy[1] * cell_next.h + cell_next.h / 2)
            pygame.draw.line(self.game.screen, c.BLUE, point1, point2, 10)

            pygame.display.update()
            sleep(0.04)
            pygame.display.update()
            # проверяет следующую клетку
            if not cell_hero:
                cell_hero = self.route_to_hero(cell_next, cells_previous)
                if not cell_hero:
                    continue
                return cell_hero + [cell]

    def move(self) -> None:
        """ Передвижение монстра по карте """
        # route = self.route1
        active_cell = self.game.map.get_cell(self.xy)
        cells = set()
        route = self.route_to_hero(active_cell, cells)
        print(route)
        route.reverse()
        print(route)
