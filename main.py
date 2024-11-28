import pygame
import numpy
from engine.game_engine import GameEngine
from engine.game_engine import Planet
from engine.game_engine import RectObstacle
from engine.game_engine import GameState

WIN_RECTANGLE = 1
LOSE_RECTANGLE = 0

engine = GameEngine()
engine.throw_velocity_constant = 500
engine.throw_radius_constant = 100
#O primeiro planeta vai ser tratado como principal e ele sempre sera o planeta com id/index 0
#planet1 = Planet(80, [400, 500], [0, 0], [0, 0], 5.0, [255, 0, 0, 255])
#planet2 = Planet(8*10**20, [600, 400], [0, 0], [0, 0], 5.0, [0, 0, 255, 255])
planet3 = Planet(8*10**19, [1000, 600], [0, 0], [0, 0], 10, [255,255,255,255])
planet4 = Planet(8*10**21, [800, 300], [0, 0], [0, 0], 4, [125, 30, 80, 255])
#engine.add_planet(planet1)
#engine.add_planet(planet2)
engine.add_planet(planet3)
engine.add_planet(planet4)
rect1 = RectObstacle(200, 300, [500, 100], WIN_RECTANGLE, [0, 255, 0, 50])
rect2 = RectObstacle(100, 100, [100, 400], LOSE_RECTANGLE, [255, 0, 0, 110])
engine.add_rect_obstacle(rect1)
engine.add_rect_obstacle(rect2)

engine.to_level(5)
#engine.load_level()
#É o relogio q controla o FPS do jogo

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
            engine.physXD.ecin.clear()
            engine.physXD.traj_x.clear()
            engine.physXD.traj_y.clear()
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
            simulation_event = engine.physXD.update()
            engine.render_sistem.draw_simulation()

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
                    
            
        case _:
            print(f"{{'\033[0;31m'}}ERROR::INVALID GAME STATE")

    clock.tick(1000)
    #Se vc quiserer q ele printe of FPS descomente a linha seguinte
    #print(clock.get_fps())

pygame.quit()