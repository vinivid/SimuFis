import numpy
import pygame
from .electric_objs import *

class PhysXD:
    #O tamanho do passo para se utilizar no método de Euler para integrais numéricas
    dt = 0.01
    movable_electric_particle = list[ElectricParticle]()
    static_electric_particle = list[ElectricParticle]()

    #Checa se o objeto a esta contido na caixa criada pelo objeto b
    #TODO: Fazer com que seja uma aproximação de um circulo em que começa a ter força pq agora é só um quadrado
    def __is_inside_radius(self, pos_obj_a : numpy.ndarray, center_obj_b : numpy.ndarray, 
                           radius_obj_b : float
                           ) -> bool:
        
        if_range_x = bool((pos_obj_a[0] >= (center_obj_b[0] - radius_obj_b)) and (pos_obj_a[0] <= (center_obj_b[0]) + radius_obj_b))
        if_range_y = bool((pos_obj_a[1] >= (center_obj_b[1] - radius_obj_b)) and (pos_obj_a[1] <= (center_obj_b[1]) + radius_obj_b))
        
        if if_range_x and if_range_y:
            return True
        else:
            return False
    
    def __update_force_particle(self, particle : ElectricParticle) -> numpy.ndarray:
        
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
        for m_particle in self.movable_electric_particle :
            m_particle.body.pos = m_particle.body.pos + m_particle.body.vel * self.dt + m_particle.body.accel * (self.dt**2 * 0.5)
            n_accel : numpy.ndarray = self.__update_force(m_particle)
            m_particle.body.vel = m_particle.body.vel + (m_particle.body.accel + n_accel) * (self.dt*0.5)
            m_particle.body.accel = n_accel

    def update(self) -> None:
        self.__velocity_verlet()