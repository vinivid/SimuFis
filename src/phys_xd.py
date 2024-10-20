import numpy
import pygame
from .electric_objs import *

class PhysXD:
    acel_calc_acumulate = list[numpy.ndarray]()

    def __init__ (self) -> None:
        self.movable_electric_particle = list[list[MovableElectricParticle, int, numpy.ndarray]]()
        self.static_electric_particle = list[FieldElectricParticle]()

    #Checa se o objeto a esta contido na caixa criada pelo objeto b
    def __is_inside_radius(self, pos_obj_a : numpy.ndarray, center_obj_b : numpy.ndarray, 
                           radius_obj_b : float
                           ) -> bool:
        
        if_range_x = bool((pos_obj_a[0] >= (center_obj_b[0] - radius_obj_b)) and (pos_obj_a[0] <= (center_obj_b[0]) + radius_obj_b))
        if_range_y = bool((pos_obj_a[1] >= (center_obj_b[1] - radius_obj_b)) and (pos_obj_a[1] <= (center_obj_b[1]) + radius_obj_b))
        
        if if_range_x and if_range_y:
            return True
        else:
            return False

    def __update_static_action(self) -> numpy.ndarray:
        force_acc = numpy.array([0,0])

        m_particle_id = int(0)
        for m_particle in self.movable_electric_particle :
            for st_particle in self.static_electric_particle :
                if self.__is_inside_radius(m_particle.pos, st_particle.pos, st_particle.max_pull_radius):
                    self.movable_electric_particle[0]
                    

    def update(self) -> None:
        self.__update_static_action()