import numpy
import pygame
from .electric_objs import MovableElectricParticle

class PhysXD:
    def __init__ (self) -> None:
        self.electric_paricles = []
        self.electro_static_objs = []

    def add_electric_particle(self, particle : MovableElectricParticle) -> None:
        self.paricles.append(particle)
