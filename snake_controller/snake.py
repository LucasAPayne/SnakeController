import pygame as pg
from square import Square


class Snake():

    def __init__(self):
        self.side_length = 100
        self.color = pg.Color('green')
        self.initialize_pos()
    
    # Resets initial values of the snake each time the game restarts
    def initialize_pos(self):
        self.x = []
        self.y = []
        self.length = 2  # if length starts at 1, the snake will collide with itself the first time it tries to grow
        self.direction = 1
        self.dead = False

        self.x.append(0)
        for i in range(1, self.length):
            self.x.append(self.x[i - 1] - self.side_length)

        for i in range(self.length):
            self.y.append(0)

    # Push each square back and overwrite the head
    # Essentially, push each square back, add a new head, and remove the old tail
    def update_position(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        # Up
        # The origin is at the top left corner of the window, so going up means the y value decreases
        if self.direction == 0:
            self.y[0] -= self.side_length

        # Right
        if self.direction == 1:
            self.x[0] += self.side_length

        # Down
        if self.direction == 2:
            self.y[0] += self.side_length

        # Left
        if self.direction == 3:
            self.x[0] -= self.side_length

    def collided_with_apple(self, apple):
        return self.x[0] == apple.x and self.y[0] == apple.y

    def collided_with_screen(self):
        display_width, display_height = pg.display.get_surface().get_size()

        # Check if x or y component of snake's head is outside screen boundaries
        return self.x[0] < 0 or self.x[0] >= display_width or self.y[0] < 0 or self.y[0] >= display_height

    def collided_with_self(self):
        for i in range(1, len(self.x)):
            if self.x[0] == self.x[i] and self.y[0] == self.y[i]:
                return True

    def grow(self, n):
        # Grow the snake by n squares
        # Put new squares on the end of the snake's tail
        # This way, the snake gets longer only when it moves, and the end of the tail does not move
        for i in range(n):
            self.x.append(self.x[-1])
            self.y.append(self.y[-1])
            self.length += 1

    def die(self):
        self.dead = True

    def draw(self):
        display = pg.display.get_surface()
        for i in range(self.length):
            pg.draw.rect(display, self.color, (self.x[i], self.y[i], self.side_length, self.side_length))
