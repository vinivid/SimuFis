from .subsystems.objs import *
from .subsystems.phys_xd import *
from .subsystems.rendering import *

class GameEngine:
    #não é necessario essa lista, mas se acabar sendo necessario ela esta aqui
    #É uma lista de planetas e id de cada um
    #O planeta de index/id 0 é o planeta principal
    planets = list[list[Planet, int]]()

    def __init__(self):
        pygame.init()
        self.physXD = PhysXD()
        #Eu lockei essa resolução para que tudo que tudo mundo fazer fique padronizado e funcionando
        self.render_sistem = Renderer(1280, 720)

    def add_planet(self, planet : Planet):
        if not self.planets:
            self.planets.append([planet, 0])
            self.physXD.planets.append([planet, 0])
            self.render_sistem.planets.append([planet, 0])
        else:
            #Acessando o id do ultimo planeta e adicionando mais 1 para o próximo id
            next_id_value = self.planets[-1][1] + 1
            self.planets.append([planet, next_id_value])
            self.physXD.planets.append([planet, next_id_value])
            self.render_sistem.planets.append([planet, next_id_value])
    
    def update_physics(self):
        self.physXD.update()
    
    def render(self):
        self.render_sistem.render()