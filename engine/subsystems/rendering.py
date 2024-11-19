import pygame
import pygame.freetype
from collections import deque

import pygame.freetype
from .objs import *
from ..game_engine import GameState
import pygame.gfxdraw

class Renderer:    
    #É uma lista de planetas e id de cada um
    #O planeta de index/id 0 é o planeta principal
    planets = list[list[Planet, int]]()
    rect_objs = list[RectObstacle]()

    #É um deque que representa a linha que segue o planeta
    trailing_line = deque[numpy.ndarray]()

    #É o raio que sera usado para renderizar os pontos em que o planeta zero esteve previamente
    previous_point_radius = 1

    #É uma lista que ira armazenar um ponto previo que o planeta esteve, esse ponto é dado após uma certa quantidade de render loops
    previus_points = list[numpy.ndarray]()

    #Por enquanto a cada 240 loops armazena um novo ponto
    qtt_loops = int(0)
    
    def __draw_pill(self, surface, color : list, button_position : tuple, dimensions : tuple) -> None:
        side_circle_radius = dimensions[1] //2

        pygame.draw.rect(surface, color, (button_position, dimensions))
        pygame.gfxdraw.filled_circle(surface, button_position[0], button_position[1] + side_circle_radius, side_circle_radius, color)
        pygame.gfxdraw.filled_circle(surface, button_position[0] + dimensions[0], button_position[1] + side_circle_radius, side_circle_radius, color)

    #Função que desenha e crie a superfíce do menu prícipal
    def __create_main_menu_surface(self) -> None:
        self.main_menu_surface.fill([0, 0, 0])

        main_menu_title, _ = self.font.render('JooJplaneta', fgcolor=[255, 255, 255, 255], bgcolor=None, rotation=0, size=100)
        main_menu_start, _ = self.font.render('Começar', fgcolor=None, bgcolor=None, rotation=0, size=40)
        main_menu_levels, _ = self.font.render('Níveis', fgcolor=None, bgcolor=None, rotation=0, size=40)
        main_menu_credits, _ = self.font.render('Créditos', fgcolor=None, bgcolor=None, rotation=0, size=40)
        main_menu_exit, _ = self.font.render('Sair', fgcolor=None, bgcolor=None, rotation=0, size=40)

        rectagle_dimensions = (300, 70)
        vertical_offset = 100

        #É o raio que sera utilizado para se criar uma circunferecia nos cantos dos retangulos de botão para criar um botão de pilula
        side_circle_radius = rectagle_dimensions[1] // 2

        start_button = (490, 250)
        levels_button = (490, vertical_offset + 250)
        credits_button = (490, vertical_offset * 2 + 250)
        exit_button = (490, vertical_offset * 3 + 250)

        #Desenha o retangulo de cada botão
        self.__draw_pill(self.main_menu_surface, [0, 255, 0], start_button, rectagle_dimensions)
        self.__draw_pill(self.main_menu_surface, [0, 255, 0], levels_button, rectagle_dimensions)
        self.__draw_pill(self.main_menu_surface, [0, 0, 255], credits_button, rectagle_dimensions)
        self.__draw_pill(self.main_menu_surface, [255, 0, 0], exit_button, rectagle_dimensions)

        #Desenha o texto na superfíce do titulo prícipal
        self.main_menu_surface.blit(main_menu_title, (370, 100))
        self.main_menu_surface.blit(main_menu_start, (start_button[0] + 85, start_button[1] + 20))
        self.main_menu_surface.blit(main_menu_levels, (levels_button[0] + 105, levels_button[1] + 20))
        self.main_menu_surface.blit(main_menu_credits, (credits_button[0] + 85, credits_button[1] + 20))
        self.main_menu_surface.blit(main_menu_exit, (exit_button[0] + 125, exit_button[1] + 20))

    #Cria a superfice em que esta desenhada a tela de game over
    def __create_game_over_surface(self) -> None:
        self.game_over_surface.fill([0, 0, 0])

        game_over_continue_text, _ = self.font.render('Continuar', fgcolor=None, bgcolor=None, rotation=0, size=60)
        game_over_main_menu_text, _ = self.font.render('Menu Principal', fgcolor=None, bgcolor=None, rotation=0, size=60)
        game_over_exit_text, _ = self.font.render('Sair', fgcolor=None, bgcolor=None, rotation=0, size=60)

        rectagle_dimensions = (400, 100)
        vertical_offset = 175

        continue_button = (440, 150)
        main_menu_button = (440, vertical_offset + 150)
        exit_button = (440, vertical_offset * 2 + 150)

        self.__draw_pill(self.game_over_surface, [0, 255, 0], continue_button, rectagle_dimensions)
        self.__draw_pill(self.game_over_surface, [0, 255, 0], main_menu_button, rectagle_dimensions)
        self.__draw_pill(self.game_over_surface, [255, 0, 0], exit_button, rectagle_dimensions)

        self.game_over_surface.blit(game_over_continue_text, (continue_button[0] + 85, continue_button[1] + 20))
        self.game_over_surface.blit(game_over_main_menu_text, (main_menu_button[0] + 7, main_menu_button[1] + 20))
        self.game_over_surface.blit(game_over_exit_text, (exit_button[0] + 140, exit_button[1] + 20))

    def __create_game_win_surface(self) -> None:
        self.game_win_surface.fill([0, 0, 0])

        game_win_continue_text, _ = self.font.render('Continuar', fgcolor=None, bgcolor=None, rotation=0, size=60)
        game_win_retry_text, _ = self.font.render('Tentar Novamente', fgcolor=None, bgcolor=None, rotation=0, size=60)
        game_win_main_menu_text, _ = self.font.render('Menu Principal', fgcolor=None, bgcolor=None, rotation=0, size=60)
        game_win_exit_text, _ = self.font.render('Sair', fgcolor=None, bgcolor=None, rotation=0, size=60)

        rectagle_dimensions = (400, 100)
        vertical_offset = 175

        continue_button = (440, 150)
        retry_button = (440, vertical_offset + 150)
        main_menu_button = (440, vertical_offset * 2 + 150)
        exit_button = (440, vertical_offset * 3 + 150)

        self.__draw_pill(self.game_win_surface, [0, 255, 0], continue_button, rectagle_dimensions)
        self.__draw_pill(self.game_win_surface, [0, 255, 0], retry_button, rectagle_dimensions)
        self.__draw_pill(self.game_win_surface, [0, 0, 255], main_menu_button, rectagle_dimensions)
        self.__draw_pill(self.game_win_surface, [255, 0, 0], exit_button, rectagle_dimensions)

        self.game_win_surface.blit(game_win_continue_text, (continue_button[0] + 85, continue_button[1] + 20))
        self.game_win_surface.blit(game_win_continue_text, (retry_button[0] + 85, retry_button[1] + 20))
        self.game_win_surface.blit(game_win_main_menu_text, (main_menu_button[0] + 7, main_menu_button[1] + 20))
        self.game_win_surface.blit(game_win_exit_text, (exit_button[0] + 140, exit_button[1] + 20))

    def __init__(self, screen_heigth : int, screen_width : int,
                 ) -> None:
        
        self.screen = pygame.display.set_mode( (screen_heigth, screen_width) )
        self.font = pygame.freetype.Font('./engine/fonts/Roboto-Regular.ttf', 12)

        self.main_menu_surface = pygame.Surface((1280, 720))
        self.__create_main_menu_surface()

        self.game_over_surface = pygame.Surface((1280, 720))
        self.__create_game_over_surface()

        self.game_win_surface = pygame.Surface((1280, 720))
        self.__create_game_win_surface()
    
    #Desenha uma flecha com base numa posição inicial e a direção q ela vai apontar
    #A direção q é o direction vector tem de ser um vetor de norma 1
    #A arrow strenght é a escala q vetor da posição vai ser desenhado
    def draw_arrow(self, arrow_color : list, ini_pos : numpy.ndarray, direction_vector: numpy.ndarray, arrow_width : int, arrow_head : float, arrow_strenght : float):
        ending_pos = ini_pos + (direction_vector * arrow_strenght)
        pygame.draw.line(self.screen, arrow_color, ini_pos, ending_pos, arrow_width)
        #Desenhando o triangulo
        #Para desenhar o tirangulo nós apenas pegamos o vetor ortogonal a direção e colocamos ele na posição final vetor da linha da seta
        #Esse vetor ortogonal vai ser um 'lado' da base para pegar o outro lado é so fazer o oposto desse vetor assim nós temos a base do nosso triangulo
        #Para fazer a altura nós fazemos uma aproximação da altura de um triangulo equilatero

        orthogonal_vec = numpy.array([direction_vector[1], - direction_vector[0]])
        #Vetores da base do triangule esquerda/direita
        basis_vector1 = ending_pos + (orthogonal_vec * (arrow_strenght * arrow_head))
        basis_vector2 = ending_pos + (-orthogonal_vec * (arrow_strenght * arrow_head))
        #Altura do triangulo para fazer um triangulo quase equilatero
        triangle_height = ending_pos + ( (direction_vector * 0.86) * ((arrow_strenght * 1/6) * 2))
        pygame.draw.polygon(self.screen, arrow_color, [basis_vector1, basis_vector2, triangle_height])

    #Desnha o vetor direção do planeta
    def __draw_accel_vector(self) -> None:
        main_planet = self.planets[0][0] 

        accel_norm = numpy.linalg.norm(main_planet.body.accel)
        point_to = main_planet.body.accel/accel_norm

            #Para que não fique uma linha gigantesca
        if accel_norm > 2000:
            self.draw_arrow([255, 255, 255, 255], main_planet.body.pos/(10**3), point_to, 2, 1/5, 20)
        else:
            self.draw_arrow([255, 255, 255, 255], main_planet.body.pos/(10**3), point_to, 2, 1/5, accel_norm/100)
    
    #Renderizar texto faz o jogo rodar em muitos menos frames protanto eu recomendo não renderizar texto enquanto o jogo ta rodando
    def __draw_main_planet_stats(self):
        main_planet = self.planets[0][0]

        self.font.render_to(self.screen, (10, 10), f'Velocidade: {numpy.linalg.norm(main_planet.body.vel)/(10**3):.4f}', [255, 255, 255])
        self.font.render_to(self.screen, (140, 10), f'km/s', [255, 255, 255])
        self.font.render_to(self.screen, (10, 25), f'Aceleração: {numpy.linalg.norm(main_planet.body.accel)/(10**3):.4f}', [255, 255, 255])
        self.font.render_to(self.screen, (140, 25), f'km/s^2', [255, 255, 255])

    #Versão do draw simulation para antes de lançar o planeta, é necessário desenhar menos coisas
    def draw_initial_simulation(self):
        self.screen.fill("black")

        self.__draw_rec_obj()

        for planet in self.planets:
            pygame.draw.circle(self.screen, planet[0].color, planet[0].body.pos/(10 ** 3), planet[0].planet_radius)
        
    def draw_simulation(self):
        self.screen.fill("black")

        if self.qtt_loops == 240:
            self.previus_points.append(self.planets[0][0].body.pos/(10 ** 3))
            self.qtt_loops = 0
        
        #Sendo o primeiro planeta o planeta pricipal armazena a posição dele
        self.trailing_line.append(self.planets[0][0].body.pos/(10 ** 3))

        self.__draw_rec_obj()
        #Guarda no deque todos os pontos atenriores até um certo número
        if len(self.trailing_line) > 70:
            self.trailing_line.popleft()

        for prev_pt in self.previus_points:
            pygame.draw.circle(self.screen, [128, 128, 128 , 170], prev_pt, self.previous_point_radius)                

        for i in range(0, len(self.trailing_line)):
            pygame.draw.circle(self.screen, self.planets[0][0].color, self.trailing_line[i], self.planets[0][0].planet_radius * (i + 1)/100)

        for planet in self.planets:
            pygame.draw.circle(self.screen, planet[0].color, planet[0].body.pos/(10 ** 3), planet[0].planet_radius)
                
        #Incrementa a quantidade de loops de renderização feitos e muda o buffer de renderização
        self.__draw_accel_vector()
        #self.draw_main_planet_stats()
        self.qtt_loops += 1

    def __draw_rec_obj(self) -> None:
        for rect in self.rect_objs:
            self.screen.blit(rect.surface, rect.pos)

    def draw_main_menu(self) -> None:
        self.screen.blit(self.main_menu_surface, (0,0))

    def draw_game_over_menu(self) -> None:
        self.screen.blit(self.game_over_surface, (0,0))

    def draw_game_win_menu(self) -> None:
        self.screen.blit(self.game_over_surface, (0, 0))