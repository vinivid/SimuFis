import pygame
from collections import deque
from .objs import *

class Renderer:
    previous_point_radius = 1
    planets = list[list[Planet, int]]()
    #É a lista que representa a linha que segue o planeta
    trailing_line = deque[numpy.ndarray]()

    #É uma lista que ira armazenar um ponto previo que o planeta esteve, esse ponto é dado após uma certa quantidade de render loops
    previus_points = list[numpy.ndarray]()

    #Por enquanto a cada 240 loops armazena um novo ponto
    qtt_loops = int()

    def __init__(self, screen_heigth : int, screen_width : int,
                 ) -> None:
        
        self.screen = pygame.display.set_mode( (screen_heigth, screen_width) )

    def render(self):
        self.screen.fill("black")

        if self.qtt_loops == 240:
            self.previus_points.append(self.planets[0][0].body.pos/(10 ** 3))
            self.qtt_loops = 0
        
        #Sendo o primeiro planeta o planeta pricipal armazena a posição dele
        self.trailing_line.append(self.planets[0][0].body.pos/(10 ** 3))

        #Guarda no deque todos os pontos atenriores até um certo número
        if len(self.trailing_line) > 70:
            self.trailing_line.popleft()

        for prev_pt in self.previus_points:
            pygame.draw.circle(self.screen, [128, 128, 128 , 170], prev_pt, self.previous_point_radius)                

        for planet in self.planets:
            pygame.draw.circle(self.screen, planet[0].color, planet[0].body.pos/(10 ** 3), planet[0].planet_radius)
        
        #Renderiza todos os pontos anteriores, como a cor da linha que segue é a mesma do planeta não há problemas em rederizar em cima dele
        for i in range(0, len(self.trailing_line)):
            pygame.draw.circle(self.screen, self.planets[0][0].color, self.trailing_line[i], self.planets[0][0].planet_radius * (i + 1)/100)
        
        #Incrementa a quantidade de loops de renderização feitos e muda o buffer de renderização
        self.qtt_loops += 1
        pygame.display.flip()
        