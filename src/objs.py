import numpy
import pygame
from enum import Enum 
from dataclasses import dataclass

@dataclass
class Body:
    #Inicializa um objeto particle com a massa dada, posição inicial e velocidade inicial (ambas como lista) raio e cor dados
    #É obrigatorio se colocar uma posição inicial
    def __init__(self, mass : float, 
                 ini_pos : list, ini_vel : list, ini_accel : list,
                 ) -> None:
        
        self.mass = mass
        self.pos = numpy.array(ini_pos)
        self.vel = numpy.array(ini_vel)
        self.accel = numpy.array(ini_accel)

@dataclass
class Planet:
    def __init__(self, mass : float,
                 ini_pos : list, ini_vel : list, ini_accel : list,
                 field_radius : float,
                 planet_radius : float
                 ) -> None:
        
        self.body = Body(mass, ini_pos, ini_vel, ini_accel)
        self.field_radius = field_radius
        self.planet_radius = planet_radius