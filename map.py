import pygame
import os
# import numpy
import random

import constants as c
from Items import Digle, Uzi, Kalashnikov, LittleCartridge, HeavyCartridge, Fraction, Mastif, Awp, Mozambyk, Knife, Bat


class Cell:
    """" Ячейка карты """
    def __init__(self, xy, walls):
        self.w = c.CELL_W
        self.h = self.w
        self.xy = tuple(xy)
        self.rect = pygame.Rect(self.xy[0], self.xy[1], self.w, self.h)
        images = [os.path.join(c.IMAGES_DIR, f"map_cell_{i}.png") for i in range(1, 7)]  # картинки рандом 1..6
        self.pic = pygame.image.load(random.choice(images))
        self.walls = set(walls)
        self.characters = list()  # hero, monster
        self.items = list()
        self.status = set()  # todo default, fire, smoke
        self.rikoshet = pygame.mixer.Sound(os.path.join(c.SOUNDS_DIR, 'rikoshet.wav'))


class Map:
    """" Карта """
    def __init__(self, screen_rect, ascii_map):
        self.cell_w = c.CELL_W
        self.cell_count_x = None  # количество ячеек по горизонтали
        self.cell_count_y = None  # количество ячеек по вертикали
        self.rect = pygame.Rect(screen_rect.x, screen_rect.y, c.CELL_W * c.CELL_COUNT_X_MAX, c.CELL_W * c.CELL_COUNT_Y_MAX)
        self.wall_w = 7  # толщина стенки
        self.wall_char = 'o'  # символ стенки в генераторе-карт
        self.line_w = 2  # толщина разделительной линии между ячейками
        self.cells = []
        self.create_from_ascii(ascii_map)

    def draw(self, screen):  # todo добавить рисовку вещей в ячейке
        """" Рисуем карту """
        for cell in self.cells:
            cell_x = cell.xy[0] * cell.w
            cell_y = cell.xy[1] * cell.h
            pic = pygame.transform.scale(cell.pic, (cell.w - self.line_w, cell.h - self.line_w))
            screen.blit(pic, (cell_x, cell_y))

        for cell in self.cells:
            cell_x = cell.xy[0] * cell.w
            cell_y = cell.xy[1] * cell.h
            if 't' in cell.walls:
                start = (cell_x, cell_y)
                end = (cell_x + cell.w, cell_y)
                pygame.draw.line(screen, c.RED_DARK, start, end, self.wall_w)
            if 'b' in cell.walls:
                start = (cell_x, cell_y + cell.w)
                end = (cell_x + cell.w, cell_y + cell.w)
                pygame.draw.line(screen, c.RED_DARK, start, end, self.wall_w)
            if 'r' in cell.walls:
                start = (cell_x + cell.w, cell_y)
                end = (cell_x + cell.w, cell_y + cell.w)
                pygame.draw.line(screen, c.RED_DARK, start, end, self.wall_w)
            if 'l' in cell.walls:
                start = (cell_x, cell_y)
                end = (cell_x, cell_y + cell.w)
                pygame.draw.line(screen, c.RED_DARK, start, end, self.wall_w)

            # рисуем вещь если она лежит на карте
            if cell.items:
                for item in cell.items:
                    item.draw(screen, cell)


    def add_charecters(self, charecters):
        """помещает персонажей на карту"""
        for charecter in charecters:
            for cell in self.cells:

                if charecter.xy[0] >= self.cell_count_x:
                    charecter.xy[0] = self.cell_count_x - 1
                if charecter.xy[1] >= self.cell_count_y:
                    charecter.xy[1] = self.cell_count_y - 1
                if charecter.xy[0] <= -1:
                    charecter.xy[0] = 0
                if charecter.xy[1] <= -1:
                    charecter.xy[1] = 0
                if tuple(charecter.xy) == cell.xy:
                    cell.characters.append(charecter)

    def add_items_to_map(self):
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

    def get_cell_by_xy(self, xy) -> "Cell":
        """ Возвращаем ячейку карты по координатам xy """
        xy = tuple(xy)
        cells = [i for i in self.cells if i.xy == xy]
        if cells:
            return cells[0]

    def create_from_ascii(self, ascii_map: str) -> "map1":
        """" Создадим карту на основе генератора карт https://notimetoplay.itch.io/ascii-mapper """
        lines = ascii_map.splitlines()  # разбиваем тект на сторки
        lines = [s for s in lines if len(s)]  # даляем пустые строки
        lines = lines[1:]  # удаляем первую стоку с адресами ячеек "0 1 2 3 4 5"

        # удаляем первый столбец с адресами ячеек "0 1 2 3 4 5"
        lines_new = []
        for line in lines:
            line = [s for s in line]
            line = line[1:]
            lines_new.append(line)
        lines = lines_new
        del lines_new

        # найдём размер карты, число рядов и столбцов
        coll_count = [len(l) for l in lines]  # длины всех сток
        coll_count = set(coll_count)  # если длины одинаковые, тогда в set только одно число
        assert len(coll_count) == 1, f"Не одинаковая длина строк: {coll_count}"  # если длины не одинаковые, тогда ошибка
        coll_count = list(coll_count)[0] // 2  # число рядов на карте, в двое меньше чем символов в строке
        row_count = len(lines) // 2  # число рядов на карте, в двое меньше чем строк
        self.cell_count_x = coll_count
        self.cell_count_y = row_count

        # создадим карту без стен
        self.cells = []
        for y in range(self.cell_count_y):
            for x in range(self.cell_count_x):
                cell = Cell((x, y), [])  # ячейка карты без стен
                self.cells.append(cell)  # добавим ячейку в карту

        # добавим стены в ячейки
        for row_id in range(len(lines)):
            if (row_id % 2) == 0:  # чётные ряды, это верхние и нижние стены
                for coll_id in range(len(lines[row_id])):
                    if (coll_id % 2) != 0:  # нечётные столбцы, это верхние и нижние стены
                        if lines[row_id][coll_id] == self.wall_char:
                            x = coll_id // 2
                            y = row_id // 2
                            cell = self.get_cell_by_xy((x, y))  # ячейка
                            if cell:  # Если ячейка найдена, добавим верхнюю стену
                                cell.walls.add('t')
                            cell_up = self.get_cell_by_xy((x, y - 1))  # ячейка сверху
                            if cell_up:  # Если ячейка сверху найдена, добавим там нижнюю стену
                                cell_up.walls.add('b')

            else:  # нечётные ряды, это левые и правые стены
                for coll_id in range(len(lines[row_id])):
                    if (coll_id % 2) == 0:  # чётные столбцы, это левые и правые стены
                        if lines[row_id][coll_id] == self.wall_char:
                            x = coll_id // 2
                            y = row_id // 2
                            cell = self.get_cell_by_xy((x, y))  # ячейка
                            if cell:  # Если ячейка найдена, добавим левую стену
                                cell.walls.add('l')
                            cell_left = self.get_cell_by_xy((x - 1, y))  # ячейка сверху
                            if cell_left:  # Если ячейка сверху найдена, добавим там нижнюю стену
                                cell_left.walls.add('r')
                    else:  # нечётные столбцы
                        pass  # центр ячейки
        return self
