""" Карта """
import random
from typing import Optional, Tuple

import pygame
from pygame import Surface
from pygame import Rect

import constants as c
from cell import Cell
from items import Digle, Uzi, Kalashnikov, LittleCartridge, HeavyCartridge, Fraction, Mastif, Awp, \
    Mozambyk, Knife, Bat, Armor_level_1, Armor_level_2, Armor_level_3, Backpack_level_1, \
    Backpack_level_2, Backpack_level_3, Medikit, Cotton


class Map:
    """ Карта """
    # noinspection PyUnresolvedReferences
    game: Optional["Game"] = None  # ссылка на игру
    name: str = ""  # название карты
    rect: Optional[Rect] = None
    cell_w: int = 0  # ширина клеток
    cell_h: int = 0  # высота клеток
    cells_x: int = 0  # количество клеток по горизонтали
    cells_y: int = 0  # количество клеток по вертикали

    def __repr__(self):
        return f"{self.name}, {self.cells_x},{self.cells_y}"

    # noinspection PyUnresolvedReferences
    def __init__(self, name: str, ascii_: str, game: "Game"):
        """ Карта
        @param name: название карты
        @param ascii_: карта в текстовом формате на основе генератора карт
        @param map: прямоугольник экрана
        """
        self.game = game
        self.name = name
        self.wall_w = 7  # толщина стенки
        self.wall_char = "o"  # символ стенки в генераторе-карт
        self.line_w = 2  # толщина разделительной линии между клетками
        self.cells = []
        self.from_ascii(ascii_)
        cell = self.cells[0]
        self.cell_w = cell.w
        self.cell_h = cell.h
        screen_rect = self.game.screen_rect()
        self.rect = pygame.Rect((screen_rect.x, screen_rect.y),
                                (self.cells_x * cell.w, self.cells_y * cell.h))

    def draw(self, screen: Surface) -> None:  # todo добавить рисовку вещей в клетке
        """ Рисует карту """
        for cell in self.cells:
            cell_x = cell.xy[0] * cell.w
            cell_y = cell.xy[1] * cell.h
            pic = pygame.transform.scale(cell.image, (cell.w - self.line_w, cell.h - self.line_w))
            screen.blit(pic, (cell_x, cell_y))

        for cell in self.cells:
            cell_x = cell.xy[0] * cell.w
            cell_y = cell.xy[1] * cell.h
            if "t" in cell.walls:
                start = (cell_x, cell_y)
                end = (cell_x + cell.w, cell_y)
                pygame.draw.line(screen, c.RED_DARK, start, end, self.wall_w)
            if "b" in cell.walls:
                start = (cell_x, cell_y + cell.w)
                end = (cell_x + cell.w, cell_y + cell.w)
                pygame.draw.line(screen, c.RED_DARK, start, end, self.wall_w)
            if "r" in cell.walls:
                start = (cell_x + cell.w, cell_y)
                end = (cell_x + cell.w, cell_y + cell.w)
                pygame.draw.line(screen, c.RED_DARK, start, end, self.wall_w)
            if "l" in cell.walls:
                start = (cell_x, cell_y)
                end = (cell_x, cell_y + cell.w)
                pygame.draw.line(screen, c.RED_DARK, start, end, self.wall_w)

            # рисует вещь если она лежит на карте
            if cell.items:
                for item in cell.items:
                    item.draw(screen, cell)

    def add_characters(self, characters):  # List[Union[Hero, Monster]]) -> None:
        """помещает персонажей на карту"""
        for character in characters:
            for cell in self.cells:
                if character.xy[0] >= self.cells_x:
                    character.xy[0] = self.cells_x - 1
                if character.xy[1] >= self.cells_y:
                    character.xy[1] = self.cells_y - 1
                if character.xy[0] <= -1:
                    character.xy[0] = 0
                if character.xy[1] <= -1:
                    character.xy[1] = 0
                if tuple(character.xy) == cell.xy:
                    cell.characters.append(character)

    def init_items(self) -> None:
        """помещает вещи на карту"""
        # сгенерим вещи из списка в заданном количестве
        obj_counts = [
            (Digle, random.randrange(1)),
            (Uzi, random.randrange(1)),
            (Kalashnikov, random.randrange(1)),
            (Mastif, random.randrange(1)),
            (LittleCartridge, random.randrange(5)),
            (HeavyCartridge, random.randrange(5)),
            (Fraction, random.randrange(5)),
            (Awp, random.randrange(1)),
            (Mozambyk, random.randrange(1)),
            (Knife, random.randrange(1)),
            (Bat, random.randrange(1))
        ]

        items = []  # сгенерированные вещи
        for obj, count in obj_counts:
            for _ in range(count):
                items.append(obj())

        # добавилм вещи на керту
        for obj in items:
            cell = random.choice(self.cells)
            cell.items.append(obj)

    def get_cell(self, xy: Tuple[int, int]) -> Optional[Cell]:
        """ return клетку карты по координатам xy """
        cells = [i for i in self.cells if i.xy == xy]
        if cells:
            return cells[0]
        return None

    def random_cell(self) -> Cell:
        """ return случайную клетку на карте """
        random_x = random.choice(range(self.cells_x))
        random_y = random.choice(range(self.cells_y))
        random_cell = self.get_cell((random_x, random_y))
        return random_cell

    def from_ascii(self, ascii_map: str) -> None:
        """ Создаёт карту на основе генератора карт https://notimetoplay.itch.io/ascii-mapper """
        lines = ascii_map.splitlines()  # разбивает тект на сторки
        lines = [s for s in lines if len(s)]  # даляет пустые строки
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
        self.cells_x = coll_count
        self.cells_y = row_count

        # создадим карту без стен
        self.cells = []
        for y in range(self.cells_y):
            for x in range(self.cells_x):
                cell = Cell((x, y), set())  # клетка карты без стен
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
                                cell.walls.add("t")
                            cell_up = self.get_cell((x, y - 1))  # клетка сверху
                            if cell_up:  # Если клетка сверху найдена, добавляет там нижнюю стену
                                cell_up.walls.add("b")

            else:  # нечётные ряды, это левые и правые стены
                for coll_id, char in enumerate(line):
                    if (coll_id % 2) == 0:  # чётные столбцы, это левые и правые стены
                        if char == self.wall_char:
                            x = coll_id // 2
                            y = row_id // 2
                            cell = self.get_cell((x, y))  # клетка
                            if cell:  # Если клетка найдена, добавляет левую стену
                                cell.walls.add("l")
                            cell_left = self.get_cell((x - 1, y))  # клетка сверху
                            if cell_left:  # Если клетка сверху найдена, добавляет там нижнюю стену
                                cell_left.walls.add("r")
                    else:  # нечётные столбцы
                        pass  # центр клетки

    def draw_xy(self, screen: Surface) -> None:
        """ рисует на карте координаты клетки xy """
        font_h = 15
        font_color = c.BLACK
        font = pygame.font.SysFont(pygame.font.get_default_font(), font_h)
        shift = 3  # сместим текс на 3 пикселя от края ячейки

        for cell in self.cells:
            # координаты клетки (x, y): top, left
            render = font.render(f"{cell.xy[0]},{cell.xy[1]}", True, font_color)
            xy1 = cell.top_left(shift)
            screen.blit(render, xy1)

            # координаты экрана (пиксели): bottom, right
            render = font.render(f"{cell.rect.right},{cell.rect.bottom}", True, font_color)
            rect2 = render.get_rect()
            xy2 = cell.bottom_right(shift)
            xy2 = (xy2[0] - rect2.w, xy2[1] - rect2.h)
            screen.blit(render, xy2)
