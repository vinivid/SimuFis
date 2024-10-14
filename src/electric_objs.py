import numpy
import pygame
from enum import Enum 

class Charge(Enum) :
    ELECTRON = 1
    PROTON = 2

class ElectricParticle:
    #Inicializa um objeto particle com a massa dada, posição inicial e velocidade inicial (ambas como lista) raio e cor dados
    #É obrigatorio se colocar uma posição inicial
    #Caso seja desejado que não tenha velocidade inicial é necessario passar uma lista de zeros
    def __init__(self, mass : float, 
                 ini_pos : list, 
                 draw_radius : float, 
                 charge : Charge, q : float,
                 ) -> None:
        
        self.mass = mass
        self.pos = numpy.array[ini_pos]
        self.draw_radius = draw_radius
        self.color
        self.charge = charge
        self.q = q

        if self.color == Charge.ELECTRON :
            self.color = [0, 0, 255, 255]
        else:
            self.color = [255, 0, 0, 255]

    #Desenha a particula no display do pygame
    def draw(self, display) -> None:
        pygame.draw.circle(display, self.color, self.pos, self.radius)

class MovableElectricParticle(ElectricParticle):
    def __init__ (self, mass : float, 
                 ini_pos : list, 
                 ini_vel : list,
                 draw_radius : float, 
                 charge : Charge, q : float,
                 ) -> None:

        ElectricParticle.__init__(mass, ini_pos, draw_radius, charge, q)

        self.ini_vel = ini_vel

    def update(self, accel : numpy.ndarray) :
        self.ini_vel = numpy.add(self.ini_vel, accel)
        self.ini_pos = numpy.add(self.ini_vel, self.ini_pos)

#Esse tipo de particula eletrica 
class FieldElectricParticle(ElectricParticle):
    def __init__ (self, mass : float, 
                 ini_pos : list, 
                 draw_radius : float,
                 
                 charge : Charge, q : float
                 ) -> None:
        
        ElectricParticle.__init__(mass, ini_pos, draw_radius, charge)
