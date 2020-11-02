""" Персонажы """

from typing import List, Tuple, NamedTuple

from character import Character

import random


class Point(NamedTuple):
    """ хоординаты на карте """
    x: int
    y: int


class Monster(Character):
    """ Монстр """
    route1: Tuple[Tuple[int, int]] = None  # маршрут снаружи дома
    route2: Tuple[Tuple[int, int]] = None  # маршрут внутри дома

    # noinspection PyUnresolvedReferences
    def __init__(self, name: str, image: str, cell_xy: List[int], actions_max: int, lives: int,
                 damage: int, game: "Game"):
        """ Монстр
        @param name: имя монстра
        @param image: картинка
        @param cell_xy: координаты клетки на карте
        @param actions_max: максимальное количество действий
        @param lives: количество здоровья
        @param damage: урон за одно действие
        @param game: ссылка на объект game
        """
        super().__init__(name, image, cell_xy, game)
        self.type = 'monster'
        self.actions_max = actions_max  # максимально количество действий монстра за один ход игры
        self.actions = 0  # количество действий на данный момент
        self.lives = lives
        self.damage = damage
        self.route1 = self.choose_route1()
        self.route2 = ((1, 1), )

    # noinspection PyUnresolvedReferences
    @classmethod
    def little(cls, name: str, cell_xy: List[int], game: "Game"):
        """ создадим маленького монстра """
        monster = cls(name=name,
                      image="little_monster.png",
                      cell_xy=cell_xy,
                      actions_max=2,
                      lives=1,
                      damage=1,
                      game=game)
        return monster

    # noinspection PyUnresolvedReferences
    @classmethod
    def big(cls, name: str, cell_xy: List[int], game: "Game"):
        """ создадим большого монстра """
        monster = cls(name=name,
                      image="big_monster.png",
                      cell_xy=cell_xy,
                      actions_max=2,
                      lives=3,
                      damage=1,
                      game=game)
        return monster

    @staticmethod
    def choose_route1() -> Tuple[Tuple[int, int]]:
        """ выбирает маршрут для монстра """
        route = [Point(1, 4), Point(2, 4), Point(3, 5)]
        for point in route:
            print(point.x)
            print(point.y)
        print(route[0].y)

        firsts_routes = [(1, 4), (2, 4)]
        for i in firsts_routes:
            print(i[0])
            print(i[1])
        print(firsts_routes[0][1])

        firsts_route = random.choice(firsts_routes)
        return firsts_route

    def move(self) -> None:
        """ Передвижение монстра по карте """
        route = self.route1
        while self.actions != 0:
            if self.cell_xy[0] != route[0]:
                if self.cell_xy[0] >= route[0]:
                    self.cell_xy[0] -= 1
                    self.actions -= 1
                elif self.cell_xy[0] <= route[0]:
                    self.cell_xy[0] += 1
                    self.actions -= 1
                elif self.cell_xy[0] == route[0]:
                    break
