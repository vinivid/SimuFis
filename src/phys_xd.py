import numpy
import pygame
from .electric_particle import electric_particle

class phys_xd():
    def __init__ (self) :
        self.electric_paricles = []
        self.electro_static_objs = []

    def add_electric_particle(self, particle : electric_particle) :
        self.paricles.append(particle)

        
