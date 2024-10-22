import pygame
from .objs import *

class Renderer:
    planets = list[list[Planet, int]]()

    def __init__(self, screen_heigth : int, screen_width : int,
                 ) -> None:
        
        self.screen = pygame.display.set_mode( (screen_heigth, screen_width) )

    def render(self):
        self.screen.fill("gray")

        for planet in self.planets:
            pygame.draw.circle(self.screen, planet[0].color, planet[0].body.pos/(10 ** 3), planet[0].planet_radius)
            
        pygame.display.flip()
        