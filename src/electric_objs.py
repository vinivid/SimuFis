import numpy
import pygame
from enum import Enum 
from dataclasses import dataclass

class Charge(Enum) :
    ELECTRON = 1
    PROTON = 2

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
class ElectricParticle:
    def __init__ (self, mass : float, 
                 ini_pos : list, ini_vel : list, ini_accel : list,
                 draw_radius : float, color : tuple[bool, list],
                 charge : Charge, q : float, force_radius : float,
                 ) -> None:

        self.body = Body(mass, ini_pos, ini_vel, ini_accel)

        self.draw_radius = draw_radius

        self.charge = charge
        self.q = q
        self.force_radius = force_radius

        self.color = [0, 0, 255, 255]
        if color[0]:
            self.color = color[1]
        else:
            if self.charge == Charge.ELECTRON :
                self.charge = [0, 0, 255, 255]
            else:
                self.charge = [255, 0, 0, 255]
