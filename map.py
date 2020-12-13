""" Карта """
import random
from typing import List, Optional, Tuple

import pygame
from pygame import Rect
from pygame import Surface
from pygame.sprite import Sprite

import settings as s
from cell import Cell

Game = "Game"


class Map(Sprite):
    """ Карта """
    cells: List[Cell] = list()
    cells_x: int = 0  # количество клеток по горизонтали
    cells_y: int = 0  # количество клеток по вертикали

    # noinspection PyUnresolvedReferences
    def __init__(self, name: str, ascii_: str, game: Game):
        """ Карта
        @param name: название карты
        @param ascii_: карта в текстовом формате на основе генератора карт
        @param map: прямоугольник экрана
        """
        super().__init__()
        self.game = game  # ссылка на игру
        self.name = name  # название карты
        self.wall_w = 7  # толщина стенки
        self.wall_char = "o"  # символ стенки в генераторе-карт
        self.line_w = 2  # толщина разделительной линии между клетками
        self.cells, self.cells_x, self.cells_y = self.from_ascii(ascii_)
        map_size = (self.cells_x * s.CELL_W, self.cells_y * s.CELL_W)
        self.size: Rect = pygame.Rect((0, 0), map_size)
        if s.SCREEN_SIZE[0] and s.SCREEN_SIZE[1]:
            map_rect = (s.SCREEN_SIZE[0] - s.DASHBOARD_W, s.SCREEN_SIZE[1])
        else:
            screen_rect = self.game.screen.get_rect()
            map_rect = (screen_rect.width - s.DASHBOARD_W, screen_rect.height)
        self.rect: Rect = pygame.Rect((0, 0), map_rect)
        self.image: Surface = pygame.image.load(s.I_MAP[name])

    def __repr__(self):
        return f"{self.name}, {self.cells_x},{self.cells_y}"

    # def draw_cells(self, screen: Surface) -> None:
    #     """ Рисует карту """
    #     for cell in self.cells:
    #         cell_x = cell.xy[0] * cell.w
    #         cell_y = cell.xy[1] * cell.h
    #         pic: Surface = pygame.transform.scale(cell.image,
    #                                               (cell.w - self.line_w, cell.h - self.line_w))
    #         screen.blit(pic, (cell_x, cell_y))
    #
    #     for cell in self.cells:
    #         cell_x = cell.xy[0] * cell.w
    #         cell_y = cell.xy[1] * cell.h
    #         if "up" in cell.walls:
    #             start = (cell_x, cell_y)
    #             end = (cell_x + cell.w, cell_y)
    #             pygame.draw.line(screen, s.RED_DARK, start, end, self.wall_w)
    #         if "down" in cell.walls:
    #             start = (cell_x, cell_y + cell.w)
    #             end = (cell_x + cell.w, cell_y + cell.w)
    #             pygame.draw.line(screen, s.RED_DARK, start, end, self.wall_w)
    #         if "right" in cell.walls:
    #             start = (cell_x + cell.w, cell_y)
    #             end = (cell_x + cell.w, cell_y + cell.w)
    #             pygame.draw.line(screen, s.RED_DARK, start, end, self.wall_w)
    #         if "left" in cell.walls:
    #             start = (cell_x, cell_y)
    #             end = (cell_x, cell_y + cell.w)
    #             pygame.draw.line(screen, s.RED_DARK, start, end, self.wall_w)

    def add_characters(self, characters):  # List[Union[Hero, Monster]]) -> None:
        """помещает персонажей на карту"""
        for character in characters:
            cell = self.get_cell(character.xy)
            cell.characters.append(character)

    def get_cell(self, xy: Tuple[int, int]) -> Optional[Cell]:
        """ return клетку карты по координатам xy """
        cells = [i for i in self.cells if i.xy == xy]
        if not cells:
            return None
        return cells[0]

    def get_direction_cell(self, cell_from: Cell, direction: str) -> Optional[Cell]:
        """ return следующую клетку из cell_from в направлении direction """
        xy_from = cell_from.xy
        xy_to = dict(
            up=(xy_from[0], xy_from[1] - 1),
            down=(xy_from[0], xy_from[1] + 1),
            left=(xy_from[0] - 1, xy_from[1]),
            right=(xy_from[0] + 1, xy_from[1]),
        ).get(direction)
        cell_to = self.get_cell(xy_to)
        return cell_to

    def get_direction_cells(self, cell_from: Cell, direction: str, distance: int) -> List[Cell]:
        """ return клетки на линии поражения direction c дальностью distance """
        xy = cell_from.xy
        cells = list()
        xy_i = None
        for i in range(distance + 1):
            # пропускаем свою клетку, она не в зоне поражения огнестрельного оружия
            if not i:
                continue
            # клетки в направлении поражения
            if direction == "up":
                xy_i = (xy[0], xy[1] - i)
            elif direction == "down":
                xy_i = (xy[0], xy[1] + i)
            elif direction == "left":
                xy_i = (xy[0] - i, xy[1])
            elif direction == "right":
                xy_i = (xy[0] + i, xy[1])
            cell = self.get_cell(xy_i)
            if cell:
                cells.append(cell)
            # дальше стенки срелять нельзя
            if direction in cell.walls:
                break
        return cells

    def random_cell(self) -> Cell:
        """ return случайную клетку на карте """
        random_x = random.choice(range(self.cells_x))
        random_y = random.choice(range(self.cells_y))
        random_cell = self.get_cell((random_x, random_y))
        return random_cell

    def from_ascii(self, ascii_map: str) -> Tuple[List[Cell], int, int]:
        """ Создаёт карту на основе генератора карт https://notimetoplay.itch.io/ascii-mapper """
        lines = ascii_map.splitlines()  # разбивает тект на сторки
        lines = [i for i in lines if len(i)]  # удаляет пустые строки
        lines = lines[1:]  # удаляет первую стоку с адресами клеток "0 1 2 3 4 5"

        # удаляет первый столбец с адресами клеток "0 1 2 3 4 5"
        lines_new = []
        for char in lines:
            char = char[1:]
            lines_new.append(char)
        lines = lines_new
        del lines_new

        # найдём размер карты, число рядов и столбцов
        coll_count = [len(i) for i in lines]  # длины всех сток
        coll_count = set(coll_count)  # если длины одинаковые, тогда в set только одно число
        assert len(coll_count) == 1, f"Не одинаковая длина строк: {coll_count}"  # если длины не
        # одинаковые, тогда ошибка
        coll_count = list(coll_count)[0] // 2  # число рядов на карте, в двое меньше чем символов
        # в строке
        row_count = len(lines) // 2  # число рядов на карте, в двое меньше чем строк
        cells_x = coll_count
        cells_y = row_count

        # создадим карту без стен
        self.cells = []
        for y in range(cells_y):
            for x in range(cells_x):
                cell = Cell(xy=(x, y), walls=set(), game=self.game)  # клетка карты без стен
                self.cells.append(cell)  # добавляет клетку в карту

        # добавляет стены в клетки
        for row_id, line in enumerate(lines):
            if (row_id % 2) == 0:  # чётные ряды, это верхние и нижние стены
                for coll_id, char in enumerate(line):
                    if (coll_id % 2) != 0:  # нечётные столбцы, это верхние и нижние стены
                        if char == self.wall_char:
                            x = coll_id // 2
                            y = row_id // 2
                            cell = self.get_cell((x, y))  # клетка
                            if cell:  # Если клетка найдена, добавляет верхнюю стену
                                cell.walls.add("up")
                            cell_up = self.get_cell((x, y - 1))  # клетка сверху
                            if cell_up:  # Если клетка сверху найдена, добавляет там нижнюю стену
                                cell_up.walls.add("down")

            else:  # нечётные ряды, это левые и правые стены
                for coll_id, char in enumerate(line):
                    if (coll_id % 2) == 0:  # чётные столбцы, это левые и правые стены
                        if char == self.wall_char:
                            x = coll_id // 2
                            y = row_id // 2
                            cell = self.get_cell((x, y))  # клетка
                            if cell:  # Если клетка найдена, добавляет левую стену
                                cell.walls.add("left")
                            cell_left = self.get_cell((x - 1, y))  # клетка сверху
                            if cell_left:  # Если клетка сверху найдена, добавляет там нижнюю стену
                                cell_left.walls.add("right")
                    else:  # нечётные столбцы
                        pass  # центр клетки
        return self.cells, cells_x, cells_y

