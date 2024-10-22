import pygame
import numpy
from engine.game_engine import GameEngine
from engine.game_engine import Planet

pygame.init()

engine = GameEngine(1280, 720)
planet1 = Planet(800000, [400, 500], [10000, 0], [0, 0], 500.0, 5.0, [255, 0, 0, 255])
planet2 = Planet(800000000000000000000, [600, 400], [0, 0], [0, 0], 500.0, 5.0, [0, 0, 255, 255])
engine.add_planet(planet1)
engine.add_planet(planet2)

clock = pygame.time.Clock()

game_loop = True

#o lop conta o prgresso no tempo
loops = 0

while game_loop:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_loop = False
    
    engine.update_physics()
    engine.render()

    #O flip muda o buffer da tela
    clock.tick(60)
    loops += 1

pygame.quit()