""" различные функции помошники """

import os
import time
import pygame
from pygame import Surface
from datetime import datetime

import settings as s
from menu import Menu


def init_screen() -> Surface:
    """ Создаёт экран игры """
    if s.SCREEN_SIZE[0] and s.SCREEN_SIZE[1]:  # окно
        screen = pygame.display.set_mode((s.SCREEN_SIZE[0], s.SCREEN_SIZE[1]))
    else:
        os.environ["SDL_VIDEO_WINDOW_POS"] = "0,0"  # полноэкранный режим
        screen = pygame.display.set_mode()
    return screen


def intro_1(screen: Surface, delay: int) -> None:
    """рисует заставку игры"""
    start_time = datetime.now()
    clock = pygame.time.Clock()
    fps = 60
    screen_rect = screen.get_rect()
    background = pygame.Surface(screen_rect.bottomright)
    background.fill(s.BROUN)

    widht = min(screen.get_rect().size)
    size = (widht, widht)
    surface = pygame.image.load(s.I_ZASTAVKA).convert()
    surface = pygame.transform.scale(surface, size)
    rect = surface.get_rect()
    rect.center = screen.get_rect().center

    while True:
        duration = datetime.now() - start_time
        duration_seconds = duration.seconds + duration.microseconds / 1000000
        alpha = int(duration_seconds * 50)  # прозрачность > 256 = black
        surface.set_alpha(alpha)

        screen.blit(background, screen_rect.topleft)
        screen.blit(surface, rect.topleft)
        if duration_seconds >= delay:
            return
        for event in pygame.event.get():
            if exit_game(event):
                pygame.quit()
        pygame.display.update()
        clock.tick(fps)


def menu_heroes(screen: Surface) -> int:
    """menu heroes"""
    menu = Menu(screen)
    clock = pygame.time.Clock()
    fps = 60
    while True:
        menu.draw()
        pygame.display.update()
        clock.tick(fps)
        for event in pygame.event.get():
            if exit_game(event):
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 1
                elif event.key == pygame.K_2:
                    return 2
                elif event.key == pygame.K_2:
                    return 3
                elif event.key == pygame.K_2:
                    return 4


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
