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
current_game_state = GameState.MENU
clock = pygame.time.Clock()

while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    match current_game_state:
        case GameState.MENU:
            level_clicked = engine.check_main_menu_click()
        
            if level_clicked != None:
                current_game_state = GameState.SIMULATE
                engine.load_level(level_clicked)

            engine.render_sistem.draw_main_menu()
        case GameState.SIMULATE:
            simulation_event = engine.physXD.update()
            engine.render_sistem.draw_simulation()

            if simulation_event != None:
                current_game_state = simulation_event
        case GameState.GAME_OVER:
            engine.render_sistem.draw_game_over_menu()
        case _:
            print(f"{{'\033[0;31m'}}ERROR::INVALID GAME STATE FOR RENDERING")

    #self.clock.tick(1000)
    #Se vc quiserer q ele printe of FPS descomente a linha seguinte
    #print(clock.get_fps())

pygame.quit()