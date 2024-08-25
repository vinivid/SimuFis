import pygame
import numpy

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

game_loop = True

#Se quisermos fazer algo um pouco mais elaborado vai ser mais facil renderizar direto em openGL
pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

x_vel = 0.5

#extra coisa

#coisa
#Esse inicio eu adquiri da documentacao do pygame, e o render loop principal
#https://www.pygame.org/docs/
while game_loop:

    pos.x += x_vel

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_loop = False

    screen.fill("gray")

    pygame.draw.circle(screen, "blue", pos, 10)

    #O flip muda o buffer da tela 
    pygame.display.flip()

    clock.tick(60)

pygame.quit()