import pygame
import random
import time

FPS = 30



pygame.init()
screen = pygame.display.set_mode([100, 100])
clock = pygame.time.Clock()


run = True
timer = 0

while run:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        print(1)
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            pygame.quit()
            break
