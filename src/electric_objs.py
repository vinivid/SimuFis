import numpy
import pygame
from enum import Enum 

class Charge(Enum) :
    ELECTRON = 1
    PROTON = 2

class ElectricParticle:
    #Inicializa um objeto particle com a massa dada, posição inicial e velocidade inicial (ambas como lista) raio e cor dados
    #É obrigatorio se colocar uma posição inicial
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
                 ini_pos : list, ini_vel : list,
                 draw_radius : float, 
                 charge : Charge, q : float,
                 ) -> None:

        ElectricParticle.__init__(mass, ini_pos, draw_radius, charge, q)
        self.ini_vel = numpy.array(ini_vel)

    def update(self, accel : numpy.ndarray) :
        self.ini_vel = numpy.add(self.ini_vel, accel)
        self.particle.pos = numpy.add(self.ini_vel, self.particle.pos)

#É uma particula elétrica com um campo que se mantem completamente estatica
class FieldElectricParticle(ElectricParticle):
    def __init__ (self, mass : float, 
                 ini_pos : list, 
                 draw_radius : float, max_pull_radius : float,
                 charge : Charge, q : float
                 ) -> None:
        
        ElectricParticle.__init__(mass, ini_pos, draw_radius, charge, q)
        self.max_pull_radius = max_pull_radius

        #TODO: adicionar uma função para dar outiline no campo eletrico 
    

#Provavelmente não sera usado mais é uma particuala que possue um campo e se move
class MovableFieldElectricParticle(FieldElectricParticle):
        def __init__ (self, mass : float, 
                 ini_pos : list, ini_vel : float,
                 draw_radius : float, max_pull_radius : float,
                 charge : Charge, q : float
                 ) -> None:

            FieldElectricParticle.__init__(mass, ini_pos, draw_radius, max_pull_radius, charge, q)
            self.ini_vel = numpy.array(ini_vel) 

        def update(self, accel : numpy.ndarray) :
            self.ini_vel = numpy.add(self.ini_vel, accel)
            self.particle.pos = numpy.add(self.ini_vel, self.particle.pos)