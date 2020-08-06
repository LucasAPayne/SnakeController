import pygame as pg
import random
from entities.square import Square


class Apple(Square):
    def __init__(self, x, y, color):
        super(Apple, self).__init__(x, y, color)
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
