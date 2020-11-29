""" Персонажы """

from datetime import datetime
from typing import Optional, Tuple

from pygame import Rect
from pygame.mixer import Channel, Sound

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

        sound = Sound(s.S_FOOTSTEPS_HERO)
        sound.set_volume(0.2)
        self.sound_footsteps = Channel(1)
        self.sound_footsteps.play(sound, loops=-1)
        self.sound_footsteps.pause()
        self.sound_damage = Sound(s.S_DAMAGE["kick"])

        self.type = ""
        self.name = name
        self.active = False
        self.items = []
        self.lives = 0
        self.damage = 0
        self.item_in_hands = None  # вещь на руках

        self.action_type = None  # move_to_cell, move_to_wall
        self.action_direction = None  # top, down, left, light
        self.action_start_time = datetime.now()  # время начала действия
        self.action_silent = False  # светофор, True запрещает начинать проигрывать звук действия
        self.actions_max = 3  # максимально количество действий героя за один ход игры
        self.actions = 0  # количество действий на данный момент
        self.armor = None

    def __repr__(self) -> str:
        line = f"{self.name}, {self.actions}/{self.actions_max}"
        if self.active:
            line += " active"
            if self.action_type:
                line += f", {self.action_type}"
            if self.action_type:
                line += f"/{self.action_direction}"
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
        self.action_type = "move_to_cell"
        self.xy = cell_to.xy
        cell_from.characters.remove(self)  # удаляем из сатрой клетки
        cell_to.characters.append(self)  # добавляем в новую клетку
        self.sound_footsteps.unpause()  # звук шагов

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

    def update(self) -> None:
        """ update """
        # двигаемся в свою клетку
        if self.action_type == "move_to_cell":
            self._update_move_to_cell()
        # двигаемся в сторону стенки
        elif self.action_type == "move_to_wall":
            self._update_move_to_wall()

    def _default_action(self) -> None:
        """ значения действия по умолчанию """
        self.action_type = None
        self.action_direction = None
        self.action_start_time = None
        self.action_silent = False

    def _update_move_to_cell(self) -> None:
        """ персонаж двигается на свою клетку """
        speed = s.SPEED
        cell = self.my_cell()
        px = cell.rect.centerx  # screen pixel x
        py = cell.rect.centery  # screen pixel y
        # меняем координаты прямоугольника персонажа по x
        diff_x = abs(self.rect.centerx - px)
        diff_x = min(speed, diff_x)
        if diff_x:
            if self.rect.centerx > px:
                self.rect.centerx -= diff_x
            elif self.rect.centerx < px:
                self.rect.centerx += diff_x
        # меняем координаты прямоугольника персонажа по y
        diff_y = abs(self.rect.centery - py)
        diff_y = min(speed, diff_y)
        if diff_y:
            if self.rect.centery > py:
                self.rect.centery -= diff_y
            elif self.rect.centery < py:
                self.rect.centery += diff_y

        # если персонаж не на своей клетке, звук шагов
        if diff_x or diff_y:
            pass
            # if not self.action_silent:
            #     Sound(s.SOUND_FOOTSTEPS_RUN2).play()
            #     self.action_silent = True
        # персонаж дошёл до своей клетки
        else:
            self._default_action()
            self.sound_footsteps.pause()

    def _update_move_to_wall(self) -> None:
        """ персонаж с низкой скоростью двигается в сторону стенки,
        издаёт звук столкновения со стеной и возвращается на свою клетку """
        # персонаж ы низкой скоростью двигается в сторону стенки
        speed = int(s.SPEED * 0.05) or 1
        if self.action_direction == "up":
            self.rect.centery -= speed
        elif self.action_direction == "down":
            self.rect.centery += speed
        elif self.action_direction == "right":
            self.rect.centerx += speed
        elif self.action_direction == "left":
            self.rect.centerx -= speed

        # звук столкновения со стеной
        time_delta = datetime.now() - self.action_start_time
        seconds = time_delta.seconds + time_delta.microseconds / 1000000
        if not self.action_silent:
            Sound(s.S_PUNCH_TO_WALL).play()
            self.action_silent = True
        # возвращается на свою клетку
        if seconds >= 0.1:
            self.action_type = "move_to_cell"

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

    def do_damage(self, damage: int) -> None:
        """ Персонаж получает урон """
        if self.armor:
            if self.armor > 0:
                self.armor -= damage
        else:
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
