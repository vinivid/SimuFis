from .subsystems.objs import *
from .subsystems.phys_xd import *
from .subsystems.rendering import *

class GameEngine:
    #não é necessario essa lista, mas se acabar sendo necessario ela esta aqui
    #É uma lista de planetas e id de cada um
    #O planeta de index/id 0 é o planeta principal
    planets = list[list[Planet, int]]()
    rect_objs = list[RectObstacle]()

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

    #Muda as caracteristacas de um planeta
    def change_planet_characteristics(self, planet_id : int, **kwargs) ->None :
        if 'vel' in kwargs:
            self.planets[planet_id] = numpy.array(kwargs['vel'])

    def update_physics(self):
        self.physXD.update()
    
    def render(self):
        self.render_sistem.render(GameState.SIMULATE)

    #Transforma os objetos que foi colocados até agora em um nível.
    def to_level(self, level_number : int) -> None:
        if level_number > 5 or level_number < 1 :
            print('O número do nível precisa ser entre 1 e 5')

        with open(f'./engine/levels/{level_number}.lv', 'w') as lv:
            for planet in self.planets:
                lv.write(f'planet {planet[0].body.mass/10**3} {planet[0].body.pos[0]/10**3} {planet[0].body.pos[1]/10**3} {planet[0].body.vel[0]} {planet[0].body.vel[1]} {planet[0].body.accel[0]} {planet[0].body.accel[1]} {planet[0].planet_radius} {planet[0].color[0]} {planet[0].color[1]} {planet[0].color[2]} {planet[0].color[3]}\n')

    #Carrega todos os objetos contidos em um nivel arquivo de nível
    #deletando os que estavam presentes no momento
    def load_level(self, level_number : int) -> None:
        #É necessario passar os dados tirando o identificador de planeta/objeto
        def read_planet(data : list) -> None:
            #transforma a lista de strings para float
            planet_to_add = Planet(float(data[0]), [float(data[1]), float(data[2])], [float(data[3]), float(data[4])], [float(data[5]), float(data[6])], float(data[7]), [int(data[8], 10), int(data[9], 10), int(data[10], 10), int(data[11], 10)])
            self.add_planet(planet_to_add)

        with open(f'./engine/levels/{level_number}.lv', 'r') as lv:
            for line in lv:
                split_line = line.split()

                if split_line[0] == 'planet':
                    read_planet(split_line[1:])
                