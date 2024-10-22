import pygame
from .objs import *

class Renderer:
    planets = list[Planet]()

    def __init__(self, screen_heigth : int, screen_width : int,
                 planets : list[Planet]
                 ) -> None:
        
        self.screen = pygame.display.set_mode( (screen_heigth, screen_width) )
        self.planets = planets

    def add_planet(self, planet : Planet):
        self.planets.append(planet)

    def render(self):
        self.screen.fill("gray")

        for planet in self.planets:
            pygame.draw.circle(self.screen, planet.color, planet.body.pos/(10 ** 3), planet.planet_radius)
            
        pygame.display.flip()
        