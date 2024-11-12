import pygame
import numpy
from engine.game_engine import GameEngine
from engine.game_engine import Planet
from engine.game_engine import RectObstacle

engine = GameEngine()
#O primeiro planeta vai ser tratado como principal e ele sempre sera o planeta com id/index 0
#planet1 = Planet(80, [400, 500], [10000, 0], [0, 0], 5.0, [255, 0, 0, 255])
#planet2 = Planet(8*10**20, [600, 400], [0, 0], [0, 0], 5.0, [0, 0, 255, 255])
#engine.add_planet(planet1)
#engine.add_planet(planet2)
#rect1 = RectObstacle(200, 300, [500, 100], 0, [0, 255, 0, 50])
#engine.add_rect_obstacle(rect1)

#engine.to_level(0)
engine.load_level(0)
#É o relogio q controla o FPS do jogo
clock = pygame.time.Clock()

game_loop = True

while game_loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_loop = False
    
    engine.update_physics()
    engine.render()

    clock.tick(1000)
    #Se vc quiserer q ele printe of FPS descomente a linha seguinte
    #print(clock.get_fps())

pygame.quit()