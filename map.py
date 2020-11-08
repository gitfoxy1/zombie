import random
from typing import List, Tuple, Union

import pygame
from pygame import Rect, Surface

import constants as c
from Items import Digle, Uzi, Kalashnikov, LittleCartridge, HeavyCartridge, Fraction, Mastif, Awp, \
    Mozambyk, Knife, Bat
from cell import Cell


class Map:
    """ Карта """

    def __init__(self, screen_rect: Rect, ascii_map: str):
        """ Карта
        @param screen_rect: прямоугольник экрана
        @param ascii_map: карта в текстовом формате на основе генератора карт
        """
        self.cell_w = c.CELL_W
        self.cell_count_x = None  # количество ячеек по горизонтали
        self.cell_count_y = None  # количество ячеек по вертикали
        self.rect = pygame.Rect(screen_rect.x, screen_rect.y, c.CELL_W * c.CELL_COUNT_X_MAX,
                                c.CELL_W * c.CELL_COUNT_Y_MAX)
        self.wall_w = 7  # толщина стенки
        self.wall_char = "o"  # символ стенки в генераторе-карт
        self.line_w = 2  # толщина разделительной линии между клетками
        self.cells = []
        self.create_from_ascii(ascii_map)

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
                if character.xy[0] >= self.cell_count_x:
                    character.xy[0] = self.cell_count_x - 1
                if character.xy[1] >= self.cell_count_y:
                    character.xy[1] = self.cell_count_y - 1
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
            (LittleCartridge, random.randrange(1)),
            (HeavyCartridge, random.randrange(1)),
            (Fraction, random.randrange(1)),
            (Awp, random.randrange(1)),
            (Mozambyk, random.randrange(1)),
            (Knife, random.randrange(20)),
            (Bat, random.randrange(20))
        ]

        items = []  # сгенерированные вещи
        for obj, count in obj_counts:
            for i in range(count):
                items.append(obj())

        # добавилм вещи на керту
        for obj in items:
            cell = random.choice(self.cells)
            cell.items.append(obj)

    def get_cell(self, xy: Union[List[int], Tuple[int, int]]) -> Cell:
        """ возвращает клетку карты по координатам xy """
        if isinstance(xy, list):
            xy = tuple(xy)
        cells = [i for i in self.cells if i.xy == xy]
        if cells:
            return cells[0]

    def create_from_ascii(self, ascii_map: str) -> "Map":
        """ Создаёт карту на основе генератора карт https://notimetoplay.itch.io/ascii-mapper """
        lines = ascii_map.splitlines()  # разбивает тект на сторки
        lines = [s for s in lines if len(s)]  # даляет пустые строки
        lines = lines[1:]  # удаляет первую стоку с адресами ячеек "0 1 2 3 4 5"

        # удаляет первый столбец с адресами ячеек "0 1 2 3 4 5"
        lines_new = []
        for line in lines:
            line = [s for s in line]
            line = line[1:]
            lines_new.append(line)
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
        self.cell_count_x = coll_count
        self.cell_count_y = row_count

        # создадим карту без стен
        self.cells = []
        for y in range(self.cell_count_y):
            for x in range(self.cell_count_x):
                cell = Cell((x, y), set())  # клетка карты без стен
                self.cells.append(cell)  # добавляет клетку в карту

        # добавляет стены в клетки
        for row_id in range(len(lines)):
            if (row_id % 2) == 0:  # чётные ряды, это верхние и нижние стены
                for coll_id in range(len(lines[row_id])):
                    if (coll_id % 2) != 0:  # нечётные столбцы, это верхние и нижние стены
                        if lines[row_id][coll_id] == self.wall_char:
                            x = coll_id // 2
                            y = row_id // 2
                            cell = self.get_cell((x, y))  # клетка
                            if cell:  # Если клетка найдена, добавляет верхнюю стену
                                cell.walls.add("t")
                            cell_up = self.get_cell((x, y - 1))  # клетка сверху
                            if cell_up:  # Если клетка сверху найдена, добавляет там нижнюю стену
                                cell_up.walls.add("b")

            else:  # нечётные ряды, это левые и правые стены
                for coll_id in range(len(lines[row_id])):
                    if (coll_id % 2) == 0:  # чётные столбцы, это левые и правые стены
                        if lines[row_id][coll_id] == self.wall_char:
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
        return self

    def draw_xy(self, screen: Surface) -> None:
        """ рисует на карте координаты клетки xy """
        font_h = 15
        font_color = c.BLACK
        font = pygame.font.SysFont(pygame.font.get_default_font(), font_h)
        shift = 0.2

        for cell in self.cells:
            # координаты клетки (x, y): top, left
            x = cell.xy[0]
            y = cell.xy[1]
            render = font.render(f"{x}, {y}", True, font_color)
            rect1 = render.get_rect()
            x1 = int(cell.rect.left + rect1.w * shift)
            y1 = int(cell.rect.top + rect1.h * shift)
            screen.blit(render, (x1, y1))

            # координаты экрана (пиксели): bottom, right
            x_screen = cell.xy[0] * cell.w  # TODO
            y_screen = cell.xy[1] * cell.h
            x_br = cell.rect.right
            y_br = cell.rect.bottom
            render = font.render(f"{x_br},{y_br}", True, font_color)
            rect2 = render.get_rect()
            x2 = int(x_br - rect2.w - rect2.w * shift)
            y2 = int(y_br - rect2.h - rect2.h * shift)
            screen.blit(render, (x2, y2))

    def draw_monster_path(self, screen: Surface) -> None:
        """ рисует на карте путь монстра """
        font_h = 100
        font_color = c.BLUE
        font = pygame.font.SysFont(pygame.font.get_default_font(), font_h)

        # координаты клетки x, y
        for cell in self.cells:
            x_tl = cell.xy[0] * cell.w
            y_tl = cell.xy[1] * cell.h
            render = font.render(f"+", True, font_color)
            rect_txt = render.get_rect()
            x_txt = x_tl + cell.w / 2 - rect_txt.w / 2
            y_txt = y_tl + cell.h / 2 - rect_txt.h / 2
            screen.blit(render, (x_txt, y_txt))
