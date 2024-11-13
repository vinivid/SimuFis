import pygame
import numpy
from engine.game_engine import GameEngine
from engine.game_engine import Planet
from engine.game_engine import RectObstacle

engine = GameEngine()
#O primeiro planeta vai ser tratado como principal e ele sempre sera o planeta com id/index 0
planet1 = Planet(80, [400, 500], [10000, 0], [0, 0], 5.0, [255, 0, 0, 255])
planet2 = Planet(8*10**20, [600, 400], [0, 0], [0, 0], 5.0, [0, 0, 255, 255])
planet3 = Planet(8*10**19, [1000, 600], [0, 0], [0, 0], 10, [255,255,255,255])
engine.add_planet(planet1)
engine.add_planet(planet2)
engine.add_planet(planet3)
rect1 = RectObstacle(200, 300, [500, 100], 0, [0, 255, 0, 50])
rect2 = RectObstacle(100, 100, [100, 400], 1, [255, 0, 0, 50])
#engine.add_rect_obstacle(rect1)
#engine.add_rect_obstacle(rect2)

engine.to_level(2)
#engine.load_level()
#É o relogio q controla o FPS do jogo
engine.game_loop()
pygame.quit()