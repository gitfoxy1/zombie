""" Персонажы """

import random
from time import sleep
from typing import List, Set, Tuple, Union

import pygame
from pygame.mixer import Channel, Sound

import settings as s
from character import Character
from map import Cell

Game = "Game"
TRoute = List[List[Cell]]


class Monster(Character):
    """ Монстр """
    route: List[Cell] = list()  # маршрут монстпа к герою

    # noinspection PyUnresolvedReferences
    def __init__(self, name: str, image: str, xy: Tuple[int, int], actions_max: int, lives: int,
                 damage: int, iq: int, game: Game):
        """ Монстр
        @param name: имя монстра
        @param image: картинка
        @param xy: координаты клетки на карте
        @param actions_max: максимальное количество действий
        @param lives: количество здоровья
        @param damage: урон за одно действие
        @param game: ссылка на объект game
        """
        super().__init__(image, xy, game)
        self.type: str = "monster"
        self.name: str = name
        self.actions_max: int = actions_max  # максимально количество действий монстра за один ход игры
        self.lives: int = lives
        self.damage: int = damage
        self.iq: int = iq

        sound = Sound(s.S_FOOTSTEPS_MONSTER)
        sound.set_volume(0.5)
        self.sound_footsteps = Channel(2)
        self.sound_footsteps.play(sound, loops=-1)
        self.sound_footsteps.pause()
        self.sound_damage: Sound = Sound(s.S_DAMAGE["kick_monster1"])

    # noinspection PyUnresolvedReferences
    @classmethod
    def little(cls, xy: Tuple[int, int], game: Game):
        """ создадим маленького монстра """
        monster = cls(name="little_monster_1",
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
    def big(cls, xy: Tuple[int, int], game: Game):
        """ создадим большого монстра """
        monster = cls(name="big_monster_1",
                      image="big_monster.png",
                      xy=xy,
                      actions_max=3,
                      lives=3,
                      damage=1,
                      iq=7,
                      game=game)
        return monster

    @classmethod
    def boss_1(cls, xy: Tuple[int, int], game: Game):
        """ создадим большого монстра """
        monster = cls(name="boss_1",
                      image="monster_boss_1.png",
                      xy=xy,
                      actions_max=3,
                      lives=10,
                      damage=1,
                      iq=10,
                      game=game)
        return monster

    @classmethod
    def fast(cls, xy: Tuple[int, int], game: Game):
        """ создадим большого монстра """
        monster = cls(name="fast",
                      image="fast_monster.png",
                      xy=xy,
                      actions_max=6,
                      lives=2,
                      damage=1,
                      iq=6,
                      game=game)
        return monster

    @classmethod
    def eye(cls, xy: Tuple[int, int], game: Game):
        """ создадим большого монстра """
        monster = cls(name="eye",
                      image="eye.png",
                      xy=xy,
                      actions_max=3,
                      lives=2,
                      damage=3,
                      iq=8,
                      game=game)
        return monster

    @classmethod
    def boss_2(cls, xy: Tuple[int, int], game: Game):
        """ создадим большого монстра """
        monster = cls(name="boss_2",
                      image="monster_boss_2.png",
                      xy=xy,
                      actions_max=6,
                      lives=10,
                      damage=1,
                      iq=11,
                      game=game)
        return monster

    @classmethod
    def shooting(cls, xy: Tuple[int, int], game: Game):
        """ создадим большого монстра """
        monster = cls(name="shooting",
                      image="shoting_monster.png",
                      xy=xy,
                      actions_max=3,
                      lives=2,
                      damage=2,
                      iq=7,
                      game=game)
        return monster

    @classmethod
    def smart(cls, xy: Tuple[int, int], game: Game):
        """ создадим большого монстра """
        monster = cls(name="smart",
                      image="smart_monster.png",
                      xy=xy,
                      actions_max=3,
                      lives=2,
                      damage=2,
                      iq=15,
                      game=game)
        return monster

    @classmethod
    def boss_3(cls, xy: Tuple[int, int], game: Game):
        """ создадим большого монстра """
        monster = cls(name="boss_3",
                      image="monster_boss_3.png",
                      xy=xy,
                      actions_max=3,
                      lives=14,
                      damage=2,
                      iq=11,
                      game=game)
        return monster

    @classmethod
    def walking(cls, xy: Tuple[int, int], game: Game):
        """ создадим большого монстра """
        monster = cls(name="walking",
                      image="walking_dead.png",
                      xy=xy,
                      actions_max=3,
                      lives=5,
                      damage=2,
                      iq=7,
                      game=game)
        return monster

    @classmethod
    def ghost(cls, xy: Tuple[int, int], game: Game):
        """ создадим большого монстра """
        monster = cls(name="ghost",
                      image="ghost.png",
                      xy=xy,
                      actions_max=3,
                      lives=2,
                      damage=2,
                      iq=11,
                      game=game)
        return monster

    @classmethod
    def boss_4(cls, xy: Tuple[int, int], game: Game):
        """ создадим большого монстра """
        monster = cls(name="boss_4",
                      image="monster_boss_4.png",
                      xy=xy,
                      actions_max=3,
                      lives=16,
                      damage=1,
                      iq=13,
                      game=game)
        return monster

    @classmethod
    def bat(cls, xy: Tuple[int, int], game: Game):
        """ создадим большого монстра """
        monster = cls(name="bat",
                      image="bat.png",
                      xy=xy,
                      actions_max=3,
                      lives=1,
                      damage=2,
                      iq=10,
                      game=game)
        return monster

    @classmethod
    def vampier(cls, xy: Tuple[int, int], game: Game):
        """ создадим большого монстра """
        monster = cls(name="vampier",
                      image="vampier.png",
                      xy=xy,
                      actions_max=3,
                      lives=3,
                      damage=1,
                      iq=12,
                      game=game)
        return monster

    @classmethod
    def boss_5(cls, xy: Tuple[int, int], game: Game):
        """ создадим большого монстра """
        monster = cls(name="boss_5",
                      image="monster_boss_5.png",
                      xy=xy,
                      actions_max=3,
                      lives=18,
                      damage=1,
                      iq=14,
                      game=game)
        return monster

    def route_to_hero(self, iq: int) -> List[Cell]:
        """ монстр ищет маршрут к герою """
        # найдём клетку в которой находится персонаж
        cell = self.my_cell()
        # получаем самый короткий путь до героя
        routes = list()
        for _ in range(iq):
            routes_i = self.random_routes_to_hero(cell)
            if routes_i:
                routes_i = sorted(routes_i, key=lambda i: len(i))
                route = routes_i[0]
                routes.append(route)
        if routes:
            routes = sorted(routes, key=lambda i: len(i))
            route = routes[0]
        else:
            route = [cell]
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
        directions = s.WALLS.copy()  # все возможные направления
        directions.difference_update(cell.walls)  # возможные направления без стен
        directions = sorted(directions)
        random.shuffle(directions)
        cell_next = None
        for direction in directions:
            # возможное направление клетка сверху
            if direction == "up":
                xy = (cell.xy[0], cell.xy[1] - 1)
                cell_next = self.game.map.get_cell(xy)
            # возможное направление клетка снизу
            elif direction == "down":
                xy = (cell.xy[0], cell.xy[1] + 1)
                cell_next = self.game.map.get_cell(xy)
            # возможное направление клетка слева
            elif direction == "left":
                xy = (cell.xy[0] - 1, cell.xy[1])
                cell_next = self.game.map.get_cell(xy)
            # возможное направление клетка справа
            elif direction == "right":
                xy = (cell.xy[0] + 1, cell.xy[1])
                cell_next = self.game.map.get_cell(xy)
            # пропускает клетку в которой уже были
            if cell_next in cells_checked:
                continue
            # draw поиск пути к герою
            if s.DEBUG:
                pygame.draw.line(self.game.screen, s.BLUE, cell.center(), cell_next.center(), 10)
                pygame.display.update()
                sleep(0.005)

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
        if not self.actions:
            return
        cell = self.my_cell()
        # выходим если есть герой на той же клетке вместе с монстром
        if cell.is_hero():
            self.route = []
            return
        # получаем самый короткий путь до героя, в зависимости от интелекта
        route = self.route_to_hero(iq=self.iq)
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
        # монстр атакует свою клетку, если на ней стоит герой
        cell = self.my_cell()
        hero = cell.get_hero()
        if hero:
            Sound(s.S_DAMAGE["kick"]).play()
            hero.do_damage(self.damage)
            self.actions -= 1
            return
        # монстр атакует соседнюю клетку, если на ней стоит герой
        if self.route and len(self.route) >= 2:
            cell = self.route[1]
            hero = cell.get_hero()
            if hero:
                self.sound_damage.play()
                hero.do_damage(self.damage)
                self.actions -= 1
                return
