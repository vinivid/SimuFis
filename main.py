import pygame
import numpy
import scipy

g_terra = 9.820738508133147

class objeto():
    def __init__(self, mass, ini_vel_x, ini_vel_y, pos_x, pos_y):
        self.tempo_vida = 0
        self.mass = mass
        self.vel_x = ini_vel_x
        self.vel_y = ini_vel_y
        self.pos_x = pos_x
        self.pos_y = pos_y

    def velocity_variation(self, time_var):
        self.pos_x += self.vel_x

        self.vel_y = (g_terra * (time_var ** 2))/2
        self.pos_y += self.vel_y

#G_constante_grav = 6.67482 * (10 **(-11))
#g_terra = (G_constante_grav * 5.972 * (10 ** 24))/ ((6.371 * (10 ** 6)) ** 2)
#print(g_terra)
g_terra = 9.820738508133147

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

game_loop = True

#Se quisermos fazer algo um pouco mais elaborado vai ser mais facil renderizar direto em openGL
#pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

#x_vel = 0.5
#extra coisa

#coisa
#Esse inicio eu adquiri da documentacao do pygame, e o render loop principal
#https://www.pygame.org/docs/
coisa1 = objeto(5, 0.5, 0, screen.get_width() / 2, screen.get_height() / 2)
loops = 0

while game_loop:
    coisa1.velocity_variation(0.0016 * loops)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_loop = False

    screen.fill("gray")

    pygame.draw.circle(screen, "blue", pygame.Vector2(coisa1.pos_x, coisa1.pos_y), 10)

    #O flip muda o buffer da tela 
    pygame.display.flip()

    clock.tick(60)
    loops += 1

pygame.quit()