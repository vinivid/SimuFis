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
#TODO: implementar texturas
#A massa é dada em kg e a posição é dada em km
class Planet:
    def __init__(self, mass : float,
                 ini_pos : list, ini_vel : list, ini_accel : list,
                 field_radius : float,
                 planet_radius : float, color : list
                 ) -> None:
        
        self.body = Body(mass * (10 ** 3), (ini_pos[0] * (10 ** 3), ini_pos[1] * (10 ** 3)), ini_vel, ini_accel)
        self.field_radius = field_radius
        self.planet_radius = planet_radius
        self.color = color