import pygame as pg


class Square:
    def __init__(self, x, y, color):
        self.side_length = 100
        self.x = x
        self.y = y
        self.color = color

    def draw(self):
        screen = pg.display.get_surface()
        pg.draw.rect(screen, self.color, (self.x, self.y, self.side_length, self.side_length))
