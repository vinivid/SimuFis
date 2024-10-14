import pygame
import numpy
from .src.phys_xd import *

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

game_loop = True

#o lop conta o prgresso no tempo
loops = 0

while game_loop:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_loop = False

    screen.fill("gray")


    #O flip muda o buffer da tela 
    pygame.display.flip()

    clock.tick(60)
    loops += 1

pygame.quit()