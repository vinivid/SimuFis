import numpy
import pygame
from enum import Enum 
from dataclasses import dataclass

WIN_RECTANGLE = 1
LOSE_RECTANGLE = 0

class GameState(Enum):
    PLOT = -4
    CREDITS = -2
    START = -1
    MAIN_MENU = 0
    LEVEL_SELECT = 1
    INITIAL_SPEED = 2
    SIMULATE = 4
    GAME_OVER = 8
    GAME_WIN = 16
    EXIT = 32

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
                 planet_radius : float, color : list
                 ) -> None:
        
        self.body = Body(mass * (10 ** 3), (ini_pos[0] * (10 ** 3), ini_pos[1] * (10 ** 3)), ini_vel, ini_accel)
        self.planet_radius = planet_radius
        self.color = color

@dataclass
class RectObstacle:
    def __init__(self, width : float, height : float,
                 pos : list, 
                 rect_type : int,
                 color : list,
                 ) -> None:
        
        self.height = height
        self.width = width
        #Não é necessario fazer um numpy array das coordenadas, más por consisntencia do código
        self.pos = numpy.array(pos)
        self.type = rect_type
        self.surface = pygame.Surface([width, height])
        self.surface.set_alpha(color[3])
        self.surface.fill(color[0:3])
        self.color = color

    def check_collision(self, planet : Planet) -> GameState | None:
        #constantes para facilitar saída
        #largemax é a maior coordenada do retangulo para a direita
        right_rect = self.pos[0] + self.width
        #largemin é a maior coordenada do retangulo para a esquerda

        height_low = self.pos[1] + self.height

        planet_pos = planet.body.pos/10**3
        #planetTop é a maior coordenada do planeta para cima
        planet_top = planet_pos[1] + planet.planet_radius
        #planetBot é a maior coordenada do planeta para baixo
        planet_bot = planet_pos[1] - planet.planet_radius
        #planetR é a maior coordenada do planeta para a direita
        planet_right = planet_pos[0] + planet.planet_radius
        #planetL é a maior coordenada do planeta para a esquerda
        planet_left = planet_pos[0] - planet.planet_radius

        if((planet_top >= self.pos[1] and planet_bot <= height_low) and (planet_left >= self.pos[0] and planet_right <= right_rect)):
            if self.type == WIN_RECTANGLE:
                return GameState.GAME_WIN
            else:
                return GameState.GAME_OVER
        #Se não detectar dentro da area retorna NONE (nenhuma das duas)
        else:
            return None
