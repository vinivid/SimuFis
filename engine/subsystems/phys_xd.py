import numpy
import pygame
from .objs import *
from scipy import constants

class PhysXD:
    #O tamanho do passo para se utilizar no método de Euler para integrais numéricas
    dt = 0.01
    planets = list[list[Planet, int]]()
    rect_objs = list[RectObstacle]()

    #TODO: Fazer a verificação de colisões
    def __colision_detect(self, planet : list[Planet, int]) -> GameState:
        if planet[1] == 0:
            for rect in self.rect_objs:
                if_collide = rect.check_collision(self.planets[0][0])

                if if_collide == GameState.GAME_WIN or if_collide == GameState.GAME_OVER:
                    print(if_collide.value)
                    return if_collide
        
        return GameState.NO_CHANGE
            
    #Calcula cada uma das forças que atuam em um corpo especifico colocando o referencial no outro objeto para que não tenhamos que negar o vetor
    def __update_force(self, planet : list[Planet, int]
                       ) -> numpy.ndarray:
        
        #Acumular as forças que são calculadas para representar a resultante
        acumulate_forces = numpy.zeros(2)

        for plt in self.planets:
            if plt[1] == planet[1] :
                continue

            absolute_distance = numpy.linalg.norm(plt[0].body.pos - planet[0].body.pos)
            force_norm = (constants.G * planet[0].body.mass * plt[0].body.mass) / absolute_distance ** 2

            x_projection = force_norm * ( (plt[0].body.pos[0] - planet[0].body.pos[0] )/absolute_distance)
            y_projection = force_norm * ( (plt[0].body.pos[1] - planet[0].body.pos[1] )/absolute_distance)

            acumulate_forces[0] += x_projection
            acumulate_forces[1] += y_projection
        
        #segunda lei de newton
        return acumulate_forces/planet[0].body.mass

    #O que esta escrito abaixo vem do método de integrar de Verlet
    #O metódo de Stormer-Verlet para calcular velocidades é um método adequado para esse projeto por ele ser o Thanos das tecnicas de integrar a velocidade
    #O que mais importa pra nós é q ele é facilmente implementavel, rapido, e numericamente estavel. É em essência o unico metódo sano q descreve nósso sistema
    #Agora as razões matematicas do pq ele é bom são as seguintes: Ele tem revesiabilidade no tempo (ok) e preserva a forma sympletica no espaço das fases (O quwe isso significa 
    # na nossa simulação é que ele não fode com a energia do sistema, matematicamente isso tem relação com manifolds e outras coisas q eu n tenho conhecimento)
    #Ele simplesmente é melhor que o metodo de euler de integração em todos os aspectos (outros como RK4 não mantém a enegia do sistema o q fode coisas relacionadas a campos), lógo usar ele
    #Também tem o método de leapfrog só q ele é goofy
    #TODO: Explicar esse algoritimo e a teoria no relatório
    def __velocity_verlet(self
                          ) -> None:
        
        for planet in self.planets :
            planet[0].body.pos = planet[0].body.pos + planet[0].body.vel * self.dt + planet[0].body.accel * (self.dt**2 * 0.5)
            self.__colision_detect(planet)
            n_accel : numpy.ndarray = self.__update_force(planet)
            planet[0].body.vel = planet[0].body.vel + (planet[0].body.accel + n_accel) * (self.dt*0.5)
            planet[0].body.accel = n_accel

    def update(self) -> None:
        self.__velocity_verlet()