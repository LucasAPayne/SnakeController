import pygame as pg
from entities.square import Square


class Snake():

    def __init__(self):
        self.initialize_pos()
    
    # Resets initial values of the snake each time the game restarts
    def initialize_pos(self):
        self.squares = [] # List of Square objects
        self.length = 2
        self.direction = 1
        self.dead = False

        self.squares.append(Square(0, 0, (pg.Color('green'))))
        for i in range(1, self.length):
            self.squares.append(Square(self.squares[i - 1].x - self.squares[i - 1].side_length, 0, pg.Color('green')))

    # Push each square back and overwrite the head
    # Essentially, push each square back, add a new head, and remove the old tail
    def update_position(self):
        for i in range(self.length - 1, 0, -1):
            self.squares[i].x = self.squares[i - 1].x
            self.squares[i].y = self.squares[i - 1].y

        # Up
        # The origin is at the top left corner of the window, so going up means the y value decreases
        if self.direction == 0:
            self.squares[0].y -= self.squares[0].side_length

        # Right
        if self.direction == 1:
            self.squares[0].x += self.squares[0].side_length

        # Down
        if self.direction == 2:
            self.squares[0].y += self.squares[0].side_length

        # Left
        if self.direction == 3:
            self.squares[0].x -= self.squares[0].side_length

    def collided_with_apple(self, apple):
        return self.squares[0].x == apple.x and self.squares[0].y == apple.y

    def collided_with_screen(self):
        display_width, display_height = pg.display.get_surface().get_size()

        # Check if x or y component of snake's head is outside screen boundaries
        return self.squares[0].x < 0 or self.squares[0].x >= display_width or self.squares[0].y < 0 or self.squares[0].y >= display_height

    def collided_with_self(self):
        for i in range(1, self.length):
            if self.squares[0].x == self.squares[i].x and self.squares[0].y == self.squares[i].y:
                return True

    def grow(self, n):
        # Grow the snake by n squares
        # Put new squares on the end of the snake's tail
        # This way, the snake gets longer only when it moves, and the end of the tail does not move
        for i in range(n):
            self.squares.append(Square(self.squares[-1].x, self.squares[-1].y, pg.Color('green')))
            self.length += 1

    def die(self):
        self.dead = True

    def draw(self):
        for i in range(self.length):
            self.squares[i].draw()
