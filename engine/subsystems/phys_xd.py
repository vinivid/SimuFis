import numpy
import pygame
from .objs import *
from scipy import constants

class PhysXD:
    #O tamanho do passo para se utilizar no método de Euler para integrais numéricas
    dt = 0.01
    planets = list[list[Planet, int]]()
    rect_objs = list[RectObstacle]()

    #Lista que salva a energia cinética
    ecin = list[numpy.floating]()

    #lista que contem a energia potencial gravitacional do sistema
    epg = list[numpy.floating]()

    #Lista que guarda os pontos da trajetória
    traj_x = list[numpy.floating]()
    traj_y = list[numpy.floating]()

    #Quantiddade de vezes que fora calculado as velocidades e uma linha discreta deles
    qtt_loops = int(0)
    discrete_sim_line = list[int]()

    #Checa se o planeta pricipal esta dentro de alguma area não permitida
    def __rect_colision_detect(self, planet : list[Planet, int]) -> GameState | None:
        if planet[1] == 0:
            for rect in self.rect_objs:
                if_collide = rect.check_collision(self.planets[0][0])

                if if_collide == GameState.GAME_WIN or if_collide == GameState.GAME_OVER:
                    return if_collide
        
        return None
    
    #Ela retorna o estado de game over caso o planeta saia da tela 
    def __border_pass(self) -> GameState | None:
        if self.planets[0][0].body.pos[0]/10**3 < 0 or self.planets[0][0].body.pos[0]/10**3 > 1280:
            return GameState.GAME_OVER
        
        if self.planets[0][0].body.pos[1]/10**3 < 0 or self.planets[0][0].body.pos[1]/10**3 > 720:
            return GameState.GAME_OVER
        
        return None
                
    #Calcula cada uma das forças que atuam em um corpo especifico colocando o referencial no outro objeto para que não tenhamos que negar o vetor
    #Retorna a acleração resultante das forças que atuam no corpo ou retorna o estado de jogo GAME_OVER se ouve uma colisão
    def __update_force(self, planet : list[Planet, int]
                       ) -> tuple[numpy.ndarray, bool]:
        
        #Acumular as forças que são calculadas para representar a resultante
        acumulate_forces = numpy.zeros(2)

        #Acumula a energia potencial gravitacional para um planeta
        epg_val = 0

        for plt in self.planets:
            if plt[1] == planet[1] :
                continue

            absolute_distance = numpy.linalg.norm(plt[0].body.pos - planet[0].body.pos)

            #Para checar se dois planetas colidiram precisamos verificar o seguinte:
            #Dada a distancia entre o centro desses dois planetas, temos que a distancia minima para que eles não estajam colidindo é o raio do primeiro
            #mais o raio do segundo planeta (quando a distancia esta nessa situação os dois planetas estão tangentes)
            #Portanto, para qualquer distância entre planetas talque a distância entre eles é < ao raio do primeiro + raio do segundo implica uma colisão
            if absolute_distance/10**3 < planet[0].planet_radius + plt[0].planet_radius:
                return absolute_distance, True

            MGm = (constants.G * planet[0].body.mass * plt[0].body.mass)
            force_norm = MGm / absolute_distance ** 2

            #Adiciona a energia potencial gravitacional no planeta principal
            if planet[1] == 0:
                epg_val += MGm/absolute_distance

            x_projection = force_norm * ( (plt[0].body.pos[0] - planet[0].body.pos[0] )/absolute_distance)
            y_projection = force_norm * ( (plt[0].body.pos[1] - planet[0].body.pos[1] )/absolute_distance)

            acumulate_forces[0] += x_projection
            acumulate_forces[1] += y_projection
        
        #coloca a energia potencial gravitacional do sistema
        if planet[1] == 0:
            self.epg.append(epg_val)

        #segunda lei de newton
        return acumulate_forces/planet[0].body.mass, False

    # O velocity verlet é o algoritimo de resolução de EDO'S númerico utilizado para resolver as EDO relacionadas a simulação.
    # O velocity verlet advem do método para resolver integrais do Stormer Verlet. Ele funciona a partir da aproximação da velocidade
    #com baixa complexidade computacional e alta precisão. A vantagem dele com relação ao metódo de verlet a partir da posição
    #é de que não é necessario amarzenar o valor da posição prévia de forma que podemos calcular a projeção da mudança de direção 
    #sem uso de memória extra ou complicações no código.
    def __velocity_verlet(self
                          ) -> None | GameState:

        #Checa se teve alguma colisão com algum retangulo
        rect_check = self.__rect_colision_detect(self.planets[0])

        #Checa se o planeta principal ultrapassou a tela
        border_check = self.__border_pass()

        #Se teve alguma colisão com retangulo retorna o estado
        if rect_check != None:
            return rect_check
        
        #Se ultrapassou a tela retorna o estado de game over
        if border_check != None:
            return border_check

        # Ínicio do velocity verlet
        for planet in self.planets :
            
            #Atualiza a posição do planeta com base apenas na velocidade prévia dele
            planet[0].body.pos = planet[0].body.pos + planet[0].body.vel * self.dt + planet[0].body.accel * (self.dt**2 * 0.5)

            #O update forces também checa se teve colisão
            n_accel, had_colision = self.__update_force(planet)

            #Se teve alguma colisão retorna o estado de game over
            if had_colision:
                return GameState.GAME_OVER
            
            #A equação equivalente do verlet de velocidade para o velet normal
            planet[0].body.vel = planet[0].body.vel + (planet[0].body.accel + n_accel) * (self.dt*0.5)

            #Aceleração se torna a nova aceleração
            planet[0].body.accel = n_accel
        
        #Adiciona a energia cínetica do planeta principal 
        self.ecin.append((numpy.linalg.norm(self.planets[0][0].body.vel)**2 * self.planets[0][0].body.mass)/2)

        #Adiciona o ponto da trajetória para que ele seja grafado depois
        self.traj_x.append((self.planets[0][0].body.pos[0])/10**3)
        self.traj_y.append( 720 - ((self.planets[0][0].body.pos[1])/10**3) )

        #Adiciona mais um ponto na discretização da simulação
        self.discrete_sim_line.append(self.qtt_loops)
        self.qtt_loops += 1

    #Simula a física do jogo por um pass
    #Retorna game over se algum planeta colidir (pode ser qualquer planeta, não apenas o player) ou se o planeta player for em um retangulo de perda
    #Retorna game win se o planeta chegar na area de vitória
    def update(self) -> None | GameState:
        return self.__velocity_verlet()