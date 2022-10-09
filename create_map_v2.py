

"""
  . map_maker      = cria o mapa (arrays convertidos em string) e mostra o mapa formatado
  . get_map_data   = pega dados do mapa vindo de "map_maker" necessários para criar "tiles" no canvas
  . Tile           = configura os atributos necessários para criar um objeto "tile"
  . insert_tile    = cria um "tile", recebendo todos os dados vindos de "get_map_data" e os insere num grupo
  . scenario_group = grupo de sprites que guarda todos os objetos "tile" criados
"""

# a_a
import pygame
# funções = [map_maker, insert_tile]
from random import choice

# a_b
pygame.init()
canvas = {'width': 1200, 'height': 600}
screen = pygame.display.set_mode((canvas['width'], canvas['height']))
clock = pygame.time.Clock()


# a_d: Cria um array convertido para string. Onde "column_amount" define quantos arrays serão criados e convertidos
def map_maker(column_amount, string_length):

    # Uma string com len() baseado no que é passado em "string_length" é inserido aqui
    row = []

    # O que é criado acima é passado para cá. Quanto maior "column_amount", + strings são enviadas para cá
    box = []

    # None = cria vazio / False = cria tile (telha/chão)
    decision = (None, None, None, None, False)

    # Exemplo do que acontece aqui: row = ['    XX   X'] -> de 10 índices: 7 None 3 False
    for index in range(column_amount):
        for each_map_index in range(string_length):
            chosen_content = choice(decision)
            if chosen_content is None:
                row.append(' ')
            elif chosen_content is False:
                row.append('X')

        # O array de exemplo acima é convertido para string: ['    XX   X'] se torna -> '    XX   X'
        row_str = ''.join(row)
        box.append(row_str)
        row.clear()

    # Se "column_amount" fosse 3, "row" seria: ['    XX   X', 'XX    X X ', 'X  XXXX   '] (3 strings com len=10)
    # Para maior legibilidade, o mapa é mostrado no loop formatado abaixo e retornado em seguida
    index_separator = ','
    print('[')
    for each_row in box:
        print(f"    '{each_row}'" + index_separator)
    print(']')
    return box


# a_e
def get_map_data(string_map, character):

    # Valor necessário na função, mas será substituída em "insert_tile"
    symbolic_temp_value = 50

    horizontal, vertical = [], []
    surface_found = 0

    for column_index, column in enumerate(string_map):
        for row_index, row in enumerate(column):
            # Informar a string que representa o caracter do chão do mapa (achando, começa uma contagem)
            if row == character:
                # Explicação importante sobre como o mapa é criado
                """
                Vamos definir que "string_map" seja o array abaixo
                    
                  map = [
                      ' X  X  X      X     X XXX  X  X     X  XX X X     ',
                      '            X  X  X   XX     X X          XXXXX   ',
                      '  X   X XX X    XXX XXX X X    X                  '
                  ]
                    
                  -> Cada índice é "column" (loop 1) (No exemplo há 3 índices)
                  -> Cada caractere interno de cada índice é "row" (loop 2) (Cada índice têm 50 caracteres = len())
                  -> Cada caractere interno de cada índice é verificado em busca de "character" (neste exemplo: X)
                  -> Achando "character" seu índice é capturado via vars internas (row_index & column_index)
                  -> Seu índice achado é multiplicado pela sua dimensão (w, h)
                  -> SUPOSIÇÕES: "row_index=4" & "column_index=7" & "w=50" & "h=50" -----> (4 * 50) & (7 * 50) 
                  -> RESULTADO: O chão encontrado é adicionado em x=200 e y=350 do CANVAS
                  -> Esse procedimento se repete a cada vez que "character=X" é achado
                """
                horizontal.append(row_index * symbolic_temp_value)
                vertical.append(column_index * symbolic_temp_value)
                surface_found += 1

    return {
        'surface_amount': surface_found, 'horizontal': horizontal, 'vertical': vertical
    }


# a_g
def insert_tile(group_box, tile_amount: int, x: list, y: list, tile_width: int, tile_height: int) -> None:

    route = 'assets/surfaces/'
    scenario_terrains = [f'{route}plat_1.gif', f'{route}plat_2.gif', f'{route}plat_3.gif', f'{route}plat_4.gif']
    for index in range(tile_amount):
        # a_f
        new_tile = Tile(
            picture_path=choice(scenario_terrains),
            x=x[index],
            y=y[index],
            w=tile_width,
            h=tile_height
        )
        group_box.add(new_tile)


# a_f
class Tile(pygame.sprite.Sprite):
    def __init__(self, picture_path, x, y, w, h):
        super().__init__()

        self.pos = {
            'x': x,
            'y': y
        }

        # Estes atributos só existem aqui, pois "self.image" exige, mas seus valores serão alterados em "insert_tile"
        self.atribs = {
            'width': w,
            'height': h
        }

        self.image = pygame.transform.scale(
            pygame.image.load(picture_path), (self.atribs['width'], self.atribs['height'])
        ).convert_alpha()

        self.rect = self.image.get_rect(center=(self.pos['x'], self.pos['y']))


# a_d
scenario = map_maker(column_amount=15, string_length=250)

# a_e: Aqui temos um dicionário com dados essenciais para "insert_tile"
scenario_data = get_map_data(string_map=scenario, character='X')

# a_g: Var array que deve receber objetos de chão encontrados. Este array é usado em "insert_tile"
scenario_group = pygame.sprite.Group()

# a_g: Com base em "tile_amount", se define quantos objetos de chão serão adicionados ao "group_box"
insert_tile(
    group_box=scenario_group,
    tile_amount=scenario_data['surface_amount'],
    x=scenario_data['horizontal'],
    y=scenario_data['vertical'],
    tile_width=choice(list(range(40, 61))),
    tile_height=choice(list(range(25, 41)))
)

while True:
    # a_c
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
    screen.fill('#222222')

    "# a_g: Isso aqui não é necessário, mas foi feito para ver o que acontece quando um grupo de sprites recebe dados"
    # print('A', scenario_group)
    # print('B', scenario_group.sprites())

    # a_h: "draw" é uma função interna da classe "pygame.sprite.Sprite"
    scenario_group.draw(screen)

    "Isso aqui não é necessário, mas foi feito para saber se os retângulos são inseridos no local certo"
    # for tile in scenario_group.sprites():
    #     # (canvas, cor, retângulo, expessura do retângulo)
    #     pygame.draw.rect(screen, 'magenta', tile.rect, 2)

    # a_c
    pygame.display.update()
    clock.tick(60)
