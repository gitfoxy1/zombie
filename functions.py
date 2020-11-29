""" различные функции помошники """

import pygame


def exit_game(event):
    """ Вйти из игры если нажат знак QUIT или кнопка ESCAPE """
    # по умолчанию игра продолжается
    exit_ = False

    # выход если нажат знак QUIT
    if event.type == pygame.QUIT:
        exit_ = True

    # выход если нажата кнопка ESCAPE
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_F4 and pygame.key.get_mods() & pygame.KMOD_ALT:
            exit_ = True

    return exit_


def get_direction(pressed_key: int) -> str:
    """ return направление, в зависимости от нажатой кнопки """
    direction = {
        pygame.K_UP: "up",
        pygame.K_DOWN: "down",
        pygame.K_RIGHT: "right",
        pygame.K_LEFT: "left",
    }.get(pressed_key, "")
    return direction
