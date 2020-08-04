import pygame as pg
import random
from square import Square


class Apple(Square):
    def __init__(self):
        self.color = pg.Color('red')
        self.x = 0
        self.y = 0
        self.spawn()

    def spawn(self):
        screen = pg.display.get_surface()
        display_width, display_height = screen.get_size()

        new_x = random.randrange(0, display_width, self.side_length)
        new_y = random.randrange(0, display_height, self.side_length)

        # apple should not spawn on itself or the snake
        while screen.get_at((new_x, new_y)) == pg.Color('red') or screen.get_at((new_x, new_y)) == pg.Color('green'):
            new_x = random.randrange(0, display_width, self.side_length)
            new_y = random.randrange(0, display_height, self.side_length)

        self.x = new_x
        self.y = new_y

    def draw(self):
        display = pg.display.get_surface()
        pg.draw.rect(display, self.color, (self.x, self.y, self.side_length, self.side_length))
