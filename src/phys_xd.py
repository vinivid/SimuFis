import numpy
import pygame
from .electric_objs import electric_particle

class phys_xd:
    def __init__ (self) -> None:
        self.electric_paricles = []
        self.electro_static_objs = []

    def add_electric_particle(self, particle : electric_particle) -> None:
        self.paricles.append(particle)
