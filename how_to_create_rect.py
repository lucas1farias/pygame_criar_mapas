

import pygame
from random import choice


pygame.init()
canvas = {'width': 1200, 'height': 600}
screen = pygame.display.set_mode((canvas['width'], canvas['height']))
clock = pygame.time.Clock()


class Rectangle:
    def __init__(self, w, h, x, y):
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.color = self.hexadecimal()
        self.image = pygame.Surface((w, h))
        self.rect = self.image.get_rect(center=(x, y))
        self.image.fill(self.color)
        self.canvas = pygame.display.get_surface()

    @staticmethod
    def hexadecimal():
        numbers = [str(integer) for integer in range(10)]
        characters = ('a.b.c.d.e.f'.split('.'))
        color = []
        for length in range(6):
            binary = choice((0, 1))
            if binary == 0:
                color.append(choice(numbers))
            elif binary == 1:
                color.append(choice(characters))
        color_str = "".join(color)
        return '#' + color_str

    def draw(self):
        self.canvas.blit(self.image, (self.x, self.y))


new_rectangle = Rectangle(w=50, h=50, x=100, y=100)
print(new_rectangle.color)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)

    screen.fill('#222222')

    new_rectangle.draw()

    pygame.display.update()
    clock.tick(60)
