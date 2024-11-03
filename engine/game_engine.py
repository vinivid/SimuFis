from .subsystems.objs import *
from .subsystems.phys_xd import *
from .subsystems.rendering import *

class GameEngine:
    planets = list[list[Planet, int]]()

    def __init__(self, screen_heigth : int,screen_width : int):
        self.physXD = PhysXD()
        self.render_sistem = Renderer(screen_heigth, screen_width)

    def add_planet(self, planet : Planet):
        if not self.planets:
            self.planets.append([planet, 0])
            self.physXD.planets.append([planet, 0])
            self.render_sistem.planets.append([planet, 0])
        else:
            next_id_value = self.planets[-1][1] + 1
            self.planets.append([planet, next_id_value])
            self.physXD.planets.append([planet, next_id_value])
            self.render_sistem.planets.append([planet, next_id_value])
    
    def update_physics(self):
        self.physXD.update()
    
    def render(self):
        self.render_sistem.render()