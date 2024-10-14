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
                 ini_pos : list, ini_vel : list, 
                 radius : float, color : list, 
                 charge : Charge) -> None:
        
        self.mass = mass
        self.pos = numpy.array[ini_pos[0], ini_pos[1]]
        self.vel = numpy.array[ini_vel[0], ini_vel[1]]
        self.radius = radius
        self.color = color
        self.charge = charge

    #Atualiza os aspectos da particula especifica dada a aceleração em uma certa posição
    def update(self, accel : numpy.ndarray) -> None:
        numpy.add(self.vel, accel)
        numpy.add(self.pos, self.vel)

    #Desenha a particula no display do pygame
    def draw(self, display : pygame.display.Surface) -> None:
        pygame.draw.circle(display, self.color, self.pos, self.radius)



class ElectroStaticObj:
    def __init__(self, mass : float, radius_of_effect : float, 
                 charge : Charge, Q : float,
                 pos : list, draw_radius : float) -> None:
        self.mass = mass 
        self.radius_of_effect = radius_of_effect
        self.charge = charge
        self.Q = Q 
        self.pos = pos 
        self.draw_radius = draw_radius

        self.color

        if charge == Charge.ELECTRON :
            self.color = [0, 0, 255, 255]

        else:
            self.color = [255, 0, 0, 255]

    def draw(self, display : pygame.display.Surface) -> None:
        pygame.draw.circle(display, self.color, self.pos, self.draw_radius)