import pygame
import numpy
from engine.game_engine import GameEngine
from engine.game_engine import Planet
from engine.game_engine import RectObstacle
from engine.game_engine import GameState

engine = GameEngine()
#O primeiro planeta vai ser tratado como principal e ele sempre sera o planeta com id/index 0
planet1 = Planet(80, [400, 500], [0, 0], [0, 0], 5.0, [255, 0, 0, 255])
planet2 = Planet(8*10**20, [600, 400], [0, 0], [0, 0], 5.0, [0, 0, 255, 255])
#planet3 = Planet(8*10**19, [1000, 600], [0, 0], [0, 0], 10, [255,255,255,255])
engine.add_planet(planet1)
engine.add_planet(planet2)
#engine.add_planet(planet3)
#rect1 = RectObstacle(200, 300, [500, 100], 0, [0, 255, 0, 50])
#rect2 = RectObstacle(100, 100, [100, 400], 1, [255, 0, 0, 50])
#engine.add_rect_obstacle(rect1)
#engine.add_rect_obstacle(rect2)

engine.to_level(3)
#engine.load_level()
#É o relogio q controla o FPS do jogo

game_running = True
current_game_state = GameState.MAIN_MENU
clock = pygame.time.Clock()

#Porque essas variaveis existem? Porque, por exemplo, no menu principal, de nível e game over é em essencia uma uma tela estatica q n precisamos ficar
#Renderizando o tempo inteiro
has_drawn_main_menu = False
has_drawn_game_over = False

while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    match current_game_state:
        case GameState.MAIN_MENU:
            has_drawn_game_over = False
            option_clicked = engine.check_main_menu_click()
        
            if option_clicked != None:
                current_game_state = option_clicked

                if current_game_state == GameState.START:
                    engine.load_level(1)
                    current_game_state = GameState.INITIAL_SPEED

            if not has_drawn_main_menu:
                engine.render_sistem.draw_main_menu()
                pygame.display.flip()
                has_drawn_main_menu = True

        case GameState.INITIAL_SPEED:
            print('asd')
            has_drawn_game_over = False
            has_drawn_main_menu = False
            engine.render_sistem.draw_simulation()
            pygame.display.flip()
            engine.initial_speed_calculate(1, 100)
            current_game_state = GameState.SIMULATE

        case GameState.SIMULATE:
            has_drawn_game_over = False
            has_drawn_main_menu = False
            simulation_event = engine.physXD.update()
            engine.render_sistem.draw_simulation()

            if simulation_event != None:
                current_game_state = simulation_event
            
            #Como a simulação de fisica esta sempre rodando precisamos sempre atualizar a tela
            pygame.display.flip()

        case GameState.GAME_OVER:
            has_drawn_main_menu = False

            option_clicked = engine.check_game_over_click()

            if option_clicked != None:
                current_game_state = option_clicked
                
                if option_clicked == GameState.INITIAL_SPEED:
                    engine.load_level(1)

            if not has_drawn_game_over:
                engine.render_sistem.draw_game_over_menu()
                pygame.display.flip()
                has_drawn_game_over = True

        case GameState.LEVEL_SELECT:
            current_game_state = GameState.MAIN_MENU

        case GameState.EXIT:
            game_running = False

        case _:
            print(f"{{'\033[0;31m'}}ERROR::INVALID GAME STATE")

    clock.tick(1000)
    #Se vc quiserer q ele printe of FPS descomente a linha seguinte
    #print(clock.get_fps())

pygame.quit()