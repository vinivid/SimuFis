from .subsystems.objs import *
from .subsystems.phys_xd import *
from .subsystems.rendering import *
from matplotlib import pyplot as plt
import matplotlib.animation as animation

class GameEngine:
    #não é necessario essa lista, mas se acabar sendo necessario ela esta aqui
    #É uma lista de planetas e id de cada um
    #O planeta de index/id 0 é o planeta principal
    planets = list[list[Planet, int]]()
    rect_objs = list[RectObstacle]()

    #inteiro que representa o raio do circulo que delimita o máximo que player pode jogar
    throw_radius_constant = int(100)
    #É um fator constante que determina a velociadade que sera jogado o planeta
    throw_velocity_constant = int(500)

    current_level = int(1)

    def __init__(self) -> None:
        pygame.init()
        self.physXD = PhysXD()
        #Eu lockei essa resolução para que tudo que tudo mundo fazer fique padronizado e funcionando
        self.render_sistem = Renderer(1280, 720)


    def add_planet(self, planet : Planet) -> None:
        if not self.planets:
            self.planets.append([planet, 0])
            self.physXD.planets.append([planet, 0])
            self.render_sistem.planets.append([planet, 0])
        else:
            #Acessando o id do ultimo planeta e adicionando mais 1 para o próximo id
            next_id_value = self.planets[-1][1] + 1
            self.planets.append([planet, next_id_value])
            self.physXD.planets.append([planet, next_id_value])
            self.render_sistem.planets.append([planet, next_id_value])
    
    #Adiciona um objeto de retangulo na game engine
    def add_rect_obstacle(self, obstacle : RectObstacle) -> None:
        self.rect_objs.append(obstacle)
        self.physXD.rect_objs.append(obstacle)
        self.render_sistem.rect_objs.append(obstacle)

    def update_physics(self) -> None:
        self.physXD.update()
    
    def render(self) -> None:
        self.render_sistem.render(GameState.SIMULATE)

    #Deleta todos os objetos de todas os módulos da engine
    def __delete_all_objs(self) -> None:
        self.planets.clear()
        self.physXD.planets.clear()
        self.render_sistem.planets.clear()
        self.rect_objs.clear()
        self.physXD.rect_objs.clear()
        self.render_sistem.rect_objs.clear()
        self.render_sistem.trailing_line.clear()
        self.render_sistem.previus_points.clear()

    #Transforma os objetos que foi colocados até agora em um nível.
    def to_level(self, level_number : int) -> None:
        with open(f'./engine/levels/{level_number}.lv', 'w') as lv:
            lv.write(f'rc {self.throw_radius_constant}\n')
            lv.write(f'vc {self.throw_velocity_constant}\n')

            for planet in self.planets:
                #Simplesmente escreve todos os dados do planeta do nível que vc tinha criado
                lv.write(f'planet {planet[0].body.mass/10**3} {planet[0].body.pos[0]/10**3} {planet[0].body.pos[1]/10**3} {planet[0].body.vel[0]} {planet[0].body.vel[1]} {planet[0].body.accel[0]} {planet[0].body.accel[1]} {planet[0].planet_radius} {planet[0].color[0]} {planet[0].color[1]} {planet[0].color[2]} {planet[0].color[3]}\n')

            for rect in self.rect_objs:
                #Escreve todos os dados do retangulo em um arquivo
                lv.write(f'rect {rect.width} {rect.height} {rect.pos[0]} {rect.pos[1]} {rect.type} {rect.color[0]} {rect.color[1]} {rect.color[2]} {rect.color[3]}\n')

    #Carrega todos os objetos contidos em um nivel arquivo de nível
    #deletando os que estavam presentes no momento
    def load_level(self, level_number : int) -> None:
        self.__delete_all_objs()
        with open(f'./engine/levels/{level_number}.lv', 'r') as lv:
            #Cada linha vai conter os dados de um planeta/rect em que a primeira palavra ira indicar se é um planeta ou um rect
            for line in lv:
                data = line.split()
                
                if data[0] == 'rc':
                    self.throw_radius_constant = int(data[1])
                
                elif data[0] == 'vc':
                    self.throw_velocity_constant = int(data[1])

                elif data[0] == 'planet':
                    #Coloca manualmente os dados do planeta e adiciona ele
                    planet_to_add = Planet(float(data[1]), [float(data[2]), float(data[3])], [float(data[4]), float(data[5])], [float(data[6]), float(data[7])], float(data[8]), [int(data[9], 10), int(data[10], 10), int(data[11], 10), int(data[12], 10)])
                    self.add_planet(planet_to_add)

                else:
                    #assim como o planeta coloca os dados manualmente no objeto de retangulo
                    rect_to_add = RectObstacle(float(data[1]), float(data[2]), [float(data[3]), float(data[4])], int(data[5], 10), [int(data[6], 10), int(data[7], 10), int(data[8],10), int(data[9],10)])
                    self.add_rect_obstacle(rect_to_add)
    
    #Checa se a area delimitado por um objeto retangular foi clicado
    def __check_rect_click(self, rect_pos : tuple, rect_width_height : tuple) -> bool:
        mouse_pos = pygame.mouse.get_pos()

        if((mouse_pos[1] >= rect_pos[1] and mouse_pos[1] <= rect_pos[1] + rect_width_height[1]) and (mouse_pos[0] >= rect_pos[0] and  mouse_pos[0] <= rect_pos[0] + rect_width_height[0])) and pygame.mouse.get_pressed()[0]:
            return True
        else: 
            return False

    #Checa se o jogador clicou em alguma das opções do menu pricipal
    def check_main_menu_click(self) -> GameState | None:
        rectagle_dimensions = (370, 70)
        vertical_offset = 100

        start_button = (455, 250)
        levels_button = (455, vertical_offset + 250)
        credits_button = (455, vertical_offset * 2 + 250)
        exit_button = (455, vertical_offset * 3 + 250)

        check_button_1 = self.__check_rect_click(start_button, rectagle_dimensions)
        check_button_2 = self.__check_rect_click(levels_button, rectagle_dimensions)
        check_button_3 = self.__check_rect_click(credits_button, rectagle_dimensions)
        check_button_4 = self.__check_rect_click(exit_button, rectagle_dimensions)

        if check_button_1:
            return GameState.START
        elif check_button_2:
            return GameState.LEVEL_SELECT
        elif check_button_3:
            return GameState.CREDITS
        elif check_button_4:
            return GameState.EXIT
        else:
            return None
    
    #Checa qual botão foi clicado na tela de game over
    def check_game_over_click(self) -> GameState | None:
        rectagle_dimensions = (400, 100)
        vertical_offset = 135

        continue_button = (440, 150)
        main_menu_button = (440, vertical_offset + 150)
        plot_button = (440, vertical_offset * 2 + 150)
        exit_button = (440, vertical_offset * 3 + 150)

        check_button_1 = self.__check_rect_click(continue_button, rectagle_dimensions)
        check_button_2 = self.__check_rect_click(main_menu_button, rectagle_dimensions)
        check_button_3 = self.__check_rect_click(plot_button, rectagle_dimensions)
        check_button_4 = self.__check_rect_click(exit_button, rectagle_dimensions)

        if check_button_1:
            return GameState.INITIAL_SPEED
        elif check_button_2:
            return GameState.MAIN_MENU
        elif check_button_3:
            return GameState.PLOT
        elif check_button_4:
            return GameState.EXIT
        else:
            return None
    
    def check_game_win_click(self) -> GameState | None: 
        rectagle_dimensions = (500, 80)
        vertical_offset = 100

        continue_button = (370, 170)
        retry_button = (370, vertical_offset + 170)
        plot_button = (370, vertical_offset * 2 + 170)
        main_menu_button = (370, vertical_offset * 3 + 170)
        exit_button = (370, vertical_offset * 4 + 170)

        check_button_1 = self.__check_rect_click(continue_button, rectagle_dimensions)
        check_button_2 = self.__check_rect_click(retry_button, rectagle_dimensions)
        check_button_3 = self.__check_rect_click(plot_button, rectagle_dimensions)
        check_button_4 = self.__check_rect_click(main_menu_button, rectagle_dimensions)
        check_button_5 = self.__check_rect_click(exit_button, rectagle_dimensions)

        if check_button_1:
            return GameState.START
        elif check_button_2:
            return GameState.LEVEL_SELECT
        elif check_button_3:
            return GameState.PLOT
        elif check_button_4:
            return GameState.MAIN_MENU
        elif check_button_5:
            return GameState.EXIT
        else:
            return None
        
    def check_select_level(self) -> int | None:
        rectagle_dimensions = (200, 200)
        horizontal_offset = 230

        button_1 = (75, 220)
        button_2 = (horizontal_offset + 75, 220)
        button_3 = (horizontal_offset * 2 + 75, 220)
        button_4 = (horizontal_offset * 3 + 75, 220)
        button_5 = (horizontal_offset * 4 + 75, 220)

        check_button_1 = self.__check_rect_click(button_1, rectagle_dimensions)
        check_button_2 = self.__check_rect_click(button_2, rectagle_dimensions)
        check_button_3 = self.__check_rect_click(button_3, rectagle_dimensions)
        check_button_4 = self.__check_rect_click(button_4, rectagle_dimensions)
        check_button_5 = self.__check_rect_click(button_5, rectagle_dimensions)

        if check_button_1:
            return 1
        elif check_button_2:
            return 2
        elif check_button_3:
            return 3
        elif check_button_4:
            return 4
        elif check_button_5:
            return 5
        else:
            return None
        
    # Calcula a velocidade incial do planeta principal com base na posição do mouse
    def initial_speed_calculate(self):
        released = False
        origin = self.planets[0][0].body.pos/10**3
        self.render_sistem.draw_initial_simulation()
        pygame.gfxdraw.aacircle(self.render_sistem.screen, int(self.planets[0][0].body.pos[0]/10**3), int(self.planets[0][0].body.pos[1]/10**3), int(self.throw_radius_constant), [255, 255, 255, 255])
        pygame.display.flip()

        while released == False:
            pygame.event.pump()

            for i in range (0, 500000):
                pygame.event.pump()

            while not pygame.mouse.get_pressed()[0]:
                pygame.event.pump() 

            while pygame.mouse.get_pressed()[0]:
                pygame.event.pump()

                mouse_pos = numpy.array(pygame.mouse.get_pos())  # Posição atual do mouse como vetor
                mouse_pos = mouse_pos - origin
                self.render_sistem.draw_initial_simulation()
                pygame.gfxdraw.aacircle(self.render_sistem.screen, int(self.planets[0][0].body.pos[0]/10**3), int(self.planets[0][0].body.pos[1]/10**3), int(self.throw_radius_constant), [255, 255, 255, 255])
                
                if numpy.linalg.norm(mouse_pos) < self.throw_radius_constant:
                    # Desenha o vetor que mostra para onde o planeta será lançado
                    self.render_sistem.draw_arrow([0, 255, 0], origin, mouse_pos/numpy.linalg.norm(mouse_pos), 2, 1/10, numpy.linalg.norm(mouse_pos))
                else:
                    self.render_sistem.draw_arrow([0, 255, 0], origin, mouse_pos/numpy.linalg.norm(mouse_pos), 2, 1/10, self.throw_radius_constant)
                
                pygame.display.flip()

            released = True

        if numpy.linalg.norm(mouse_pos) < self.throw_radius_constant:
            # Atualiza a velocidade do planeta
            self.planets[0][0].body.vel = (mouse_pos) * self.throw_velocity_constant 
        else:
            self.planets[0][0].body.vel = (mouse_pos/numpy.linalg.norm(mouse_pos) * self.throw_radius_constant) * self.throw_velocity_constant
                
        return GameState.SIMULATE
    
    def plot_energies(self) -> None:
        fig, ax = plt.subplots()
        ax.plot(self.physXD.discrete_sim_line, self.physXD.epg, label=f'Energia potêncial gravitacional')[0]
        ax.plot(self.physXD.discrete_sim_line, self.physXD.ecin, label=f'Energia cinética')[0]
        ax.set(xlabel='Frame da simulação', ylabel='Energias')
        ax.legend()
        plt.show()