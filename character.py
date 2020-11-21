""" Персонажы """

from typing import Optional, Tuple

from pygame import Rect

import settings as s
from cell import Cell
from sprite_on_map import SpriteOnMap

Game = "Game"


class Character(SpriteOnMap):
    """ Персонаж, класс-родитель для героя и монстра """
    # noinspection PyUnresolvedReferences
    type: Optional[str] = ""  # тип персонажа: "hero", "monster"
    name: str = ""  # имя персонажа
    active: bool = False  # True= персонаж активный, может действовать; False= не активный, ждёт

    def __init__(self, name: str, image: str, xy: Tuple[int, int], game: Game):
        self.game: Game = game  # ссылка на игру

        scale = 0.9
        width = int(s.CELL_W * scale)
        size = (width, width)
        super().__init__(image, size)
        self.xy = xy
        self.rect = self.get_rect()  # Sprite.rect

        self.type = None
        self.name = name
        self.active = False
        self.items = []
        self.lives = None
        self.item_in_hands = None  # вещь на руках

        self.actions_max = 3  # максимально количество действий героя за один ход игры
        self.actions = 0  # количество действий на данный момент

    def __repr__(self) -> str:
        line = f"{self.name}, {self.actions}/{self.actions_max}"
        if self.active:
            line += " active"
        return line

    def my_cell(self) -> Cell:
        """ return клетку в которой находится персонаж """
        cell = self.game.map.get_cell(self.xy)
        return cell

    def move_to_cell(self, cell_to: Cell) -> None:
        """ Передвижение персонажа в клету"""
        # найдём клетку в которой находится персонаж
        cell_from = self.game.map.get_cell(self.xy)

        # перемещаеме персонаж в другую клетку на карте
        self.xy = cell_to.xy
        cell_from.characters.remove(self)  # удаляем из сатрой клетки
        cell_to.characters.append(self)  # добавляем в новую клетку

    def get_rect(self) -> Rect:
        """ Sprite.rect на экране (пиксели) в центр клетки """
        rect: Rect = self.image.get_rect()
        # координаты клетки на экрана в пикселях
        px = s.CELL_W * self.xy[0]
        py = s.CELL_W * self.xy[1]
        # координаты героя на экрана, центр героя в центре клетки
        rect.x = px + s.CELL_W / 2 - rect.w / 2
        rect.y = py + s.CELL_W / 2 - rect.h / 2
        return rect

    def update(self):
        """ update """
        speed = s.SPEED
        cell = self.my_cell()

        px = cell.rect.centerx
        py = cell.rect.centery
        # если в клетке несколько героев, нарисуем их по диогонали todo
        # shift = 3
        # if len(cell.characters) >= 1 and cell.characters[0] != self:
        #     for i, character in enumerate(cell.characters):
        #         if character != self:
        #             continue
        #         if i == 0:
        #             px = cell.rect.centerx - shift
        #             py = cell.rect.centery - shift
        #         elif i == 1:
        #             px = cell.rect.centerx + shift
        #             py = cell.rect.centery + shift

        # x
        diff_x = abs(self.rect.centerx - px)
        diff_x = min(speed, diff_x)
        if diff_x:
            if self.rect.centerx > px:
                self.rect.centerx -= diff_x
            elif self.rect.centerx < px:
                self.rect.centerx += diff_x
        # y
        diff_y = abs(self.rect.centery - py)
        diff_y = min(speed, diff_y)
        if diff_y:
            if self.rect.centery > py:
                self.rect.centery -= diff_y
            elif self.rect.centery < py:
                self.rect.centery += diff_y

    def death(self) -> None:
        """ Персонаж умирает, удаляем из игры """
        # удаляет героя с карты, вещи героя сбрасывает на карту
        cell = self.my_cell()
        cell.characters.remove(self)
        for item in self.items:
            cell.append_item(item)

        # удаляет героя из игры
        self.game.heroes.remove(self)
        self.game.monsters.remove(self)
        self.game.characters.remove(self)

    def damage(self, damage: int) -> None:
        """ Персонаж получает урон """
        self.lives -= damage
        if self.lives <= 0:
            self.death()

    def end_turn(self) -> None:
        """ ход/turn закончился actions=0, персонаж становится пасивным """
        self.active = False
        self.actions = 0

    def start_turn(self) -> None:
        """ персонаж становится активным, начинается его ход/turn """
        self.active = True
        self.actions = self.actions_max
