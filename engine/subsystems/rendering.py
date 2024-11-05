import pygame
import pygame.freetype
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

    #Constantes que representam se deve desenhar a seta na posição da UI ou no planeta principal

    def __init__(self, screen_heigth : int, screen_width : int,
                 ) -> None:
        
        self.screen = pygame.display.set_mode( (screen_heigth, screen_width) )
        self.font = pygame.freetype.Font('./engine/fonts/Roboto-Regular.ttf', 12)
    
    #Desenha uma flecha com base numa posição inicial e a direção q ela vai apontar
    #A direção q é o direction vector tem de ser um vetor de norma 1
    #A arrow strenght é a escala q vetor da posição vai ser desenhado
    def draw_arrow(self, arrow_color : list, ini_pos : numpy.ndarray, direction_vector: numpy.ndarray, arrow_width : int, arrow_strenght : float):
        ending_pos = ini_pos + (direction_vector * arrow_strenght)
        pygame.draw.line(self.screen, arrow_color, ini_pos, ending_pos, arrow_width)
        #Desenhando o triangulo
        #Para desenhar o tirangulo nós apenas pegamos o vetor ortogonal a direção e colocamos ele na posição final vetor da linha da seta
        #Esse vetor ortogonal vai ser um 'lado' da base para pegar o outro lado é so fazer o oposto desse vetor assim nós temos a base do nosso triangulo
        #Para fazer a altura nós fazemos uma aproximação da altura de um triangulo equilatero

        orthogonal_vec = numpy.array([direction_vector[1], - direction_vector[0]])
        #Vetores da base do triangule esquerda/direita
        basis_vector1 = ending_pos + (orthogonal_vec * (arrow_strenght * 1/5))
        basis_vector2 = ending_pos + (-orthogonal_vec * (arrow_strenght * 1/5))
        #Altura do triangulo para fazer um triangulo quase equilatero
        triangle_height = ending_pos + ( (direction_vector * 0.86) * ((arrow_strenght * 1/6) * 2))
        pygame.draw.polygon(self.screen, arrow_color, [basis_vector1, basis_vector2, triangle_height])

    #Desnha o vetor direção do planeta
    def draw_accel_vector(self) -> None:
        main_planet = self.planets[0][0] 

        accel_norm = numpy.linalg.norm(main_planet.body.accel)
        point_to = main_planet.body.accel/accel_norm

            #Para que não fique uma linha gigantesca
        if accel_norm > 2000:
            self.draw_arrow([255, 255, 255, 255], main_planet.body.pos/(10**3), point_to, 2, 20)
        else:
            self.draw_arrow([255, 255, 255, 255], main_planet.body.pos/(10**3), point_to, 2, accel_norm/100)
    
    #Renderizar texto faz o jogo rodar em muitos menos frames protanto eu recomendo não renderizar texto enquanto o jogo ta rodando
    def draw_main_planet_stats(self):
        main_planet = self.planets[0][0]

        self.font.render_to(self.screen, (10, 10), f'Velocidade: {numpy.linalg.norm(main_planet.body.vel)/(10**3):.4f}', [255, 255, 255])
        self.font.render_to(self.screen, (140, 10), f'km/s', [255, 255, 255])
        self.font.render_to(self.screen, (10, 25), f'Aceleração: {numpy.linalg.norm(main_planet.body.accel)/(10**3):.4f}', [255, 255, 255])
        self.font.render_to(self.screen, (140, 25), f'km/s^2', [255, 255, 255])

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
        self.draw_accel_vector()
        #self.draw_main_planet_stats()
        self.qtt_loops += 1
        pygame.display.flip()
        