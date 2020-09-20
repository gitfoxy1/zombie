import pygame
import constants as c


class Text:
    """ текст """
    def __init__(self):
        # self.font = "consolas"
        self.font = "Comic Sans MS"
        # self.font = "a_AlternaSw"
        self.color = c.RED_DARK
        self.size = 30

    def draw_header1_center(self, text, screen, x, y):
        """ Пишем загловок в центре """
        size = int(self.size * 2)
        font = pygame.font.SysFont(self.font, size)
        font.set_underline(True)
        font.set_bold(True)
        render = font.render(text, True, self.color)
        text_rect = render.get_rect()
        xy = (x - text_rect.centerx, y)
        screen.blit(render, xy)
        box_rect = pygame.Rect(xy, text_rect.size)
        # pygame.draw.rect(screen, c.BLUE, box_rect, 1)
        return box_rect

    def draw_header2_left(self, text, screen, x, y):
        """ Пишем загловок слела """
        size = int(self.size * 1.5)
        font = pygame.font.SysFont(self.font, size)
        font.set_underline(True)
        font.set_bold(True)
        render = font.render(text, True, self.color)
        text_rect = render.get_rect()
        xy = (x + size * 0.2, y)
        screen.blit(render, xy)
        box_rect = pygame.Rect(xy, text_rect.size)
        # pygame.draw.rect(screen, c.BLUE, box_rect, 1)
        return box_rect

    def draw_list(self, lines, screen, x, y):
        """ Пишем список строк """
        size = self.size
        font = pygame.font.SysFont(self.font, size)
        font.set_underline(False)
        font.set_bold(False)
        box_w = int()
        box_h = int()
        for i in range(len(lines)):
            text = lines[i]
            render = font.render(text, True, self.color)
            text_rect = render.get_rect()
            y_i = y + size * i
            xy = (x, y_i)
            screen.blit(render, xy)
            # pygame.draw.rect(screen, c.BLUE, (xy, text_rect.size), 1)
            box_w = max(box_w, text_rect.w)
            box_h = y_i + text_rect.h
            print()
        box_rect = pygame.Rect((x, y), (box_w, box_h - y))
        # pygame.draw.rect(screen, c.BLUE, box_rect, 1)
        return box_rect