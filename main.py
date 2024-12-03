import pygame
import numpy
from engine.game_engine import GameEngine
from engine.game_engine import Planet
from engine.game_engine import RectObstacle
from engine.game_engine import GameState

WIN_RECTANGLE = 1
LOSE_RECTANGLE = 0

engine = GameEngine()

#Como criar níveis:
#COLOCAR CONSTANTES DE VELOCIDADE E RAIO NO JOGAR DO PLANETA
#Para se mudar as constantes de jogar os planetas é necessario mudar 
#o trhow_velocity_constant e o throw_radius_constant ambas pertencentes a engine
#O trhow_velocity_constant é a constante multiplicativa de jogar o planeta quando o
#player solta o mouse.
#O throw_radius_constant é a constante que determina o raio do player jogar o planeta
#A velocidade na qual o planeta sera jogado depende de ambas essas constantes.
#Exemplo de como coloca-las abaixo:
#
#engine.throw_velocity_constant = 400
#engine.throw_radius_constant = 100
#
#COLOCAR PLANETAS
#Você instancia os planeatas que deseja colocar criando um objeto de planeta
#Por exemplo:
#
# planet1 = Planet(9*10**19, [100, 350], [0, 0], [0, 0], 10, [255,255,255,255])
# engine.add_planet(planet1)
#
#tera esse planeta no nível que você deseja fazer.
#O primeiro planeta adicionado sera considerado o planeta do jogador, tenha isso em mente.
#
#COLOCAR OS RETANGULOS
#Análogo ao colocar um planeta. Exemplo abaixo:
#
# rect1 = RectObstacle(200, 200, [1000, 250], WIN_RECTANGLE, [0, 255, 0, 50])
# engine.add_rect_obstacle(rect1)
#
#SOBERE O TO LEVEL !!IMPORTANTE!!
# a função engine.to_level(numero_do_nivel_a_ser_criado) transforma o q fora adicionado em nível
# ela deve ser chamada após adicionar todos os objetos que deseja colocar no nível
# Exemplo: para criar o nível três após colocar os objetos é necessario apenas colcoar
# 
# engine.to_level(3)
# 
# criar outros níves após isso não dara certo.
# 
# CUIDADO PARA NÃO SOBRE ESCREVER O NÍVEL DOS OUTROS, CASO ISSO OCORRA MUDE PARA O QUE ESTAVA ANTERIORMENTE
# ANTES DE PUSHAR
# A area abaixo delimitada por //// é a necessaria para se criar um nível, não é necessario escrever
# nada além dela assim como n é necessario colocar mais de um to_level() (se vc fizer isso vai bugar)
# ////////////////////////////////////////////////////////////////////////////////////////////////////

engine.throw_velocity_constant = 3500
engine.throw_radius_constant = 120

planet1 = Planet(1, [400, 600], [0, 0], [0, 0], 5, [43, 67, 88, 255])
planet2 = Planet(10**24, [0, 0], [0, 0], [0, 0], 500, [211, 129, 21, 255])
#planet3 = Planet(100, [600, 350], [0, 100000], [0, 0], 2, [211, 211, 211, 255])

engine.add_planet(planet1)
engine.add_planet(planet2)
#engine.add_planet(planet3)

rect1 = RectObstacle(80, 80, [900, 0], WIN_RECTANGLE, [0, 255, 0, 50])
rect2 = RectObstacle(500, 50, [600, 360], LOSE_RECTANGLE, [255, 0, 0, 80])

engine.add_rect_obstacle(rect1)
engine.add_rect_obstacle(rect2)

engine.to_level(5)
#////////////////////////////////////////////////////////////////////////////////////////////////////////

game_running = True
current_game_state = GameState.MAIN_MENU
clock = pygame.time.Clock()

#Porque essas variaveis existem? Porque, por exemplo, no menu principal, de nível e game over é em essencia uma uma tela estatica q n precisamos ficar
#Renderizando o tempo inteiro
has_drawn_main_menu = False
has_drawn_game_over = False
has_drawn_game_win = False
has_drawn_level_select = False
has_pumped = False
has_pumped_level = False
has_draw_credits = False

while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    match current_game_state:
        case GameState.MAIN_MENU:
            engine.current_level = 1
            has_pumped_level = False
            has_drawn_game_over = False
            has_drawn_game_win = False
            has_drawn_level_select = False
            has_draw_credits = False
            #É necessario dar pump para tirar o problema de cliclar instantaneamente

            if not has_drawn_main_menu:
                engine.render_sistem.draw_main_menu()
                pygame.display.flip()
                has_drawn_main_menu = True 

            if not has_pumped:
                for i in range (0, 500000):
                    pygame.event.pump()
                has_pumped = True

            option_clicked = engine.check_main_menu_click()

            if option_clicked != None:
                current_game_state = option_clicked

            if not has_drawn_main_menu:
                engine.render_sistem.draw_main_menu()
                pygame.display.flip()
                has_drawn_main_menu = True
            

        case GameState.START:
                engine.load_level(engine.current_level)
                current_game_state = GameState.INITIAL_SPEED

        case GameState.INITIAL_SPEED:
            has_pumped = False
            has_drawn_level_select = False
            has_drawn_game_over = False
            has_drawn_main_menu = False
            has_drawn_game_win = False
            has_pumped_level = False
            has_draw_credits = False

            engine.physXD.ecin.clear()
            engine.physXD.traj_x.clear()
            engine.physXD.traj_y.clear()
            engine.physXD.epg.clear()
            engine.physXD.discrete_sim_line.clear()
            engine.physXD.qtt_loops = 0
            current_game_state = engine.initial_speed_calculate()

        case GameState.SIMULATE:
            has_pumped = False
            has_drawn_level_select = False
            has_drawn_game_over = False
            has_drawn_main_menu = False
            has_drawn_game_win = False
            has_pumped_level = False
            has_draw_credits = False

            simulation_event = engine.physXD.update()
            engine.render_sistem.draw_simulation()

            if engine.check_ff_button():
                current_game_state = GameState.GAME_OVER

            if simulation_event != None:
                current_game_state = simulation_event
            
            #Como a simulação de fisica esta sempre rodando precisamos sempre atualizar a tela
            pygame.display.flip()

        case GameState.GAME_OVER:
            has_pumped = False
            has_pumped_level = False
            has_drawn_level_select = False
            has_drawn_main_menu = False
            has_drawn_game_win = False
            has_draw_credits = False

            option_clicked = engine.check_game_over_click()

            if option_clicked != None:
                if option_clicked == GameState.PLOT:
                    engine.plot_energies()

                    for i in range (0, 500000):
                        pygame.event.pump()
                else:
                    current_game_state = option_clicked
                
                if option_clicked == GameState.INITIAL_SPEED:
                    engine.load_level(engine.current_level)

            if not has_drawn_game_over:
                engine.render_sistem.draw_game_over_menu()
                pygame.display.flip()
                has_drawn_game_over = True
            

        case GameState.LEVEL_SELECT:
            has_drawn_main_menu = False
            has_drawn_game_win = False
            has_drawn_game_over = False
            has_draw_credits = False

            if not has_drawn_level_select:
                engine.render_sistem.draw_level_screen()
                pygame.display.flip()  
                has_drawn_level_select = True          

            if not has_pumped_level:
                for i in range (0, 400000):
                    pygame.event.pump()
                has_pumped_level = True

            #Muda para o nível se algum nível foi selecionado
            level_selected = engine.check_select_level()
            
            if level_selected != None:
                engine.current_level = level_selected
                current_game_state = GameState.START

        case GameState.EXIT:
            game_running = False

        case GameState.GAME_WIN:
            has_pumped = False
            has_drawn_level_select = False
            has_drawn_game_over = False
            has_drawn_main_menu = False
            has_pumped_level = False
            has_draw_credits = False

            option_clicked = engine.check_game_win_click()
            
            if not has_drawn_game_win:
                engine.render_sistem.draw_game_win_menu()
                pygame.display.flip()
                has_drawn_game_win = True

            if option_clicked != None:
                if option_clicked == GameState.PLOT:
                    engine.plot_energies()

                    for i in range (0, 500000):
                        pygame.event.pump()
                else:
                    current_game_state = option_clicked

                #Vai para o próximo nível somente se o próximo nível não for o 6, se n retorna para o 1
                if current_game_state == GameState.START:
                    if engine.current_level < 5:
                        engine.current_level = engine.current_level + 1
                    else:
                        engine.current_level = 1

                elif current_game_state == GameState.LEVEL_SELECT:
                    current_game_state = GameState.START
            
        case GameState.CREDITS:
            has_pumped = False
            has_drawn_level_select = False
            has_drawn_game_over = False
            has_drawn_main_menu = False
            has_pumped_level = False

            if not has_draw_credits:
                engine.render_sistem.draw_credits()
                has_draw_credits = True
                pygame.display.flip()

            if engine.check_ff_button():
                current_game_state = GameState.MAIN_MENU            

        case _:
            print(f"{{'\033[0;31m'}}ERROR::INVALID GAME STATE")

    clock.tick(1000)
    #Se vc quiserer q ele printe of FPS descomente a linha seguinte
    #print(clock.get_fps())

pygame.quit()