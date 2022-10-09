

"""
"EXEMPLO DE MAPA COM STRING DE 28 COLUNAS"
# scenario = [
#     '                            ',
#     '                            ',
#     '                            ',
#     ' XX    XXX             XX   ',
#     ' XX',
#     'XXXX            XX        XX',
#     'XXXX          XX            ',
#     'XX     X  XXXX      XX  XX  ',
#     '       X  XXXX      XX  XXX ',
#     '     XXX  XXXXXX    XX  XXXX',
#     'XXXXXXXX  XXXXXX    XX  XXXX',
# ]

# Criação do mapa em forma de string (passado antes do loop)

========== RASCUNHOS ==========
# print(scenario)
# print('---------------------------------------------------------------------------------------------------------------')
# print(scenario_proper)

# horizontal, vertical = [], []
# x_found = []
# for column_index, column in enumerate(scenario):
#     for row_index, row in enumerate(column):
#         if row == 'X':
#             x_found.append(None)
#             horizontal.append(row_index * 50)
#             vertical.append(column_index * 50)
# print(len(x_found), len(horizontal), len(vertical))

# sprite_box = ['terrain.png', 'terrain2.png']
# tile_objects_group = pygame.sprite.Group()
# for index in range(len(x_found)):
#     new_tile = Tile(choice(sprite_box), horizontal[index], vertical[index])
#     tile_objects_group.add(new_tile)
# print(tile_objects_group)
"""

import pygame
from random import choice


def map_maker(repeat_it, string_length):
    """ ================================================ def map_maker ================================================
    A. O loop aninhado cria uma string com uma sequência de 'X' e '', inseridos na var 'row'
    B. Quando 'row' alcança o valor em 'string_length', essa sequência é guardada em 'box'
    C. SUPOSIÇÃO:
       string_length = 10    chosen = 'X' ou ''    row = ['X', '', '', '', 'X', 'X', 'X', '', 'X', 'X']
    D. O que é gerado em 'row' é reconvertido p/ string e armazenado em 'box', ou seja:    box = ['X   XXX XX']
    E. A var 'row' é zerada e o loop matriz se repete com base no valor passado em 'repeat_it', alimentando 'box'
    F. Então, 'box' receberá um novo grupo de strings até 'repeat_it' alcançar seu valor estipulado
    G. SUPOSIÇÃO:                  0           , 1           , 2
       repeat_it = 3    box = ['X   XXX XX', 'XXXX X   X', '  XX XXXXX']
    """

    row = []
    box = []
    decision = ([], [], [], [], [], [0])  # [] == + chance de criar espaços em branco

    loop_counter = 0
    end = False
    counter = repeat_it

    while loop_counter < repeat_it:       # quantas linhas o cenário terá (altura)

        while len(row) < string_length:
            chosen = choice(decision)
            if chosen:
                row.append('X')
            else:
                row.append(' ')

        row_str = ''.join(row)
        box.append(row_str)
        loop_counter += 1
        row.clear()
    "return box"  # DESATIVADO

    # Final do loop - Editar última linha para ter + chance de haver chão
    end = True
    if end:
        # print('Cheguei aqui')
        last_row = []
        decision = (0, 1, 1, 2)
        for number in range(counter):
            chosen = choice(decision)
            if chosen == 0:
                last_row.append(' ')
            elif chosen == 1:
                last_row.append('X')
            else:
                last_row.append('X  ')
        last_row = "".join(last_row)
        box[-1] = last_row
    return box


def map_handler(string_map, character):
    """ ============================================== def map_x_handler ==============================================
    Achar o caracter usado p/ criar um mapa na sua posição vertical e horizontal e conta quantos foram criados
    """
    horizontal, vertical = [], []

    x_found = 0
    for column_index, column in enumerate(string_map):
        for row_index, row in enumerate(column):
            if row == character:
                horizontal.append(row_index * 50)   # Onde está da <- p/ ->
                vertical.append(column_index * 50)  # Onde está de cima p/ baixo
                x_found += 1  # Quantos
    # print(len(x_found), len(horizontal), len(vertical))
    return {
        'x_found': x_found, 'horizontal': horizontal, 'vertical': vertical
    }


def insert_tile(group_box, tile_amount: int, where_x_at_horizontal: list, where_x_at_vertical: list) -> None:
    """ =============================================== def insert_tile ===============================================
    Após ter o mapa string a localização dos caracteres, esses dados são passados p/ objetos p/ inserção no Canvas
    :param group_box:             grupo criado p/ receber objetos da classe "Tile", criados nesta função
    :param tile_amount:           quantidade de caracteres que a função "map_x_handler" achar
    :param where_x_at_horizontal: coordenada do caracter que a função "map_x_handler" achar (<- p/ ->)
    :param where_x_at_vertical:   coordenada do caracter que a função "map_x_handler" achar (cima p/ baixo)
    :return: None
    """
    for index in range(tile_amount):
        new_tile = Tile(
            picture_path=choice(scenario_terrains),
            x=where_x_at_horizontal[index],
            y=where_x_at_vertical[index]
        )
        group_box.add(new_tile)


def map_proper_format(string_map):
    """ ============================================ def map_proper_format ============================================
    Salvar mapa criado (via "map_maker") no formato correto e pronto p/ copiar p/ projeto
    """
    map_as_str = []
    for string_group in string_map:
        map_as_str.append(f"'{string_group}',")
    for index in map_as_str:
        print(index)
    return map_as_str


class Tile(pygame.sprite.Sprite):
    def __init__(self, picture_path, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(pygame.image.load(picture_path), (45, 45)).convert_alpha()
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.image2 = pygame.image.load(picture_path)
        self.image2_width = self.image2.get_width()
        self.image2_height = self.image2.get_height()
        print(self.image2_height)
        print(self.image2_width)
        # self.image = pygame.Surface((size, size))
        # self.image.fill('cyan')


pygame.init()
screen = pygame.display.set_mode((1200, 600))
clock = pygame.time.Clock()

"CRIAÇÃO DO PRIMEIRO MAPA"
# Parâmetros determinados pelas dimensões do CANVAS / tamanho da telha
scenario = map_maker(repeat_it=11, string_length=250)
scenario_proper = map_proper_format(string_map=scenario)
scenario_terrains = ['terrain.png', 'terrain2.png']
scenario_group = pygame.sprite.Group()
map_setup = map_handler(string_map=scenario, character='X')

insert_tile(
    group_box=scenario_group,
    tile_amount=map_setup['x_found'],
    where_x_at_horizontal=map_setup['horizontal'],
    where_x_at_vertical=map_setup['vertical']
)

print(scenario_proper)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
    screen.fill('#222222')

    scenario_group.draw(screen)
    for tile in scenario_group.sprites():
        pygame.draw.rect(screen, 'orangered', tile.rect, 2)

    pygame.display.update()
    clock.tick(60)
