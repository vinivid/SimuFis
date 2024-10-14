import numpy
import pygame
from enum import Enum 

class charge(Enum) :
    electron = 1
    proton = 2

class electric_particle():
    #Inicializa um objeto particle com a massa dada, posição inicial e velocidade inicial (ambas como lista) raio e cor dados
    #É obrigatorio se colocar uma posição inicial
    #Caso seja desejado que não tenha velocidade inicial é necessario passar uma lista de zeros
    def __init__(self, mass : float, ini_pos : list, ini_vel : list, radius : float, color : float, charge : charge):
        self.mass = mass
        self.pos = numpy.array[ini_pos[0], ini_pos[1]]
        self.vel = numpy.array[ini_vel[0], ini_vel[1]]
        self.radius = radius
        self.color = color
        self.charge = charge

    #Atualiza os aspectos da particula especifica dada a aceleração em uma certa posição
    def update(self, accel : numpy.ndarray):
        numpy.add(self.vel, accel)
        numpy.add(self.pos, self.vel)

    #Desenha a particula no display do pygame
    def draw_particle(self, display):
        pygame.draw.circle(display, self.color, self.pos, self.radius)