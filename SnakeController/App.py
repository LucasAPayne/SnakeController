import pygame as pg
import sys
import threading

from Apple import Apple
from Graph import Graph
from Snake import Snake


class App:
    def __init__(self):
        self.display_width = 600
        self.display_height = 600
        self.display_center = ((self.display_width / 2), (self.display_height / 2))

        self.finished_loading = False

        self.input_list = []
        self.current_input = 0

        pg.init()
        pg.display.set_mode((self.display_width, self.display_height))
        pg.display.set_caption("Snake Controller")

        self.apple = Apple()
        self.graph = Graph()
        self.snake = Snake()

    #############
    ### Input ###
    #############

    def generate_input_list(self):
        #initialize to bogus values
        self.input_list = [-1 for i in range(len(self.graph.path) - 1)]

        # Each element in the input list corresponds to the direction the snake should move
        for i in range(len(self.graph.path) - 1):
            # Up
            # Since the graph has a grid layout, the numbers of vertical nodes differ by the size of a row of the graph
            if self.graph.path[i + 1] == self.graph.path[i] - self.graph.row_size:
                self.input_list[i] = 0

            # Right
            # If the next node in the path is numbered one more than the current node, the snake should move to the right
            # No need to check if the next node wraps to the next row because they are not adjacent
            elif self.graph.path[i + 1] == self.graph.path[i] + 1:
                self.input_list[i] = 1

            # Down
            elif self.graph.path[i + 1] == self.graph.path[i] + self.graph.row_size:
                self.input_list[i] = 2

            # Left
            elif self.graph.path[i + 1] == self.graph.path[i] - 1:
                self.input_list[i] = 3

    def simulate_input(self):
        self.snake.direction = self.input_list[self.current_input]
        self.current_input += 1

        if self.current_input >= len(self.graph.path) - 1:
            self.current_input = 0

    def poll_exit(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit(0)

    ##################
    ### Game Logic ###
    ##################

    def check_collision(self):
        if self.snake.collided_with_apple(self.apple):
            self.snake.grow(1)
            self.apple.spawn()

        if self.snake.collided_with_screen() or self.snake.collided_with_self():
            self.snake.die()
            
    #################
    ### Rendering ###
    #################

    def display_message(self, message, location):
        font = pg.font.SysFont('consolas', 30)
        text_surface = font.render(message, True, pg.Color('white'))
        text_rect = text_surface.get_rect()
        text_rect.center = location
        pg.display.get_surface().blit(text_surface, text_rect)

    def draw_gridlines(self):
        pg.display.get_surface().fill(pg.Color('white'))
        squares = int(self.display_width / self.snake.side_length)
        for x in range(squares):
            for y in range(squares):
                pg.draw.rect(pg.display.get_surface(), pg.Color('black'), (x * self.snake.side_length, y * self.snake.side_length, self.snake.side_length - 1, self.snake.side_length - 1))

    def draw_frame(self):
        pg.display.get_surface().fill(pg.Color('black'))
        self.draw_gridlines()
        self.apple.draw()
        self.snake.draw()
        pg.display.update()

    ###################
    ### Game States ###
    ###################

    def run(self):
        pg.display.get_surface().fill(pg.Color('black'))
        intro = True

        self.display_message('Press Space to Start', self.display_center)

        while intro:
            self.poll_exit()
            keys = pg.key.get_pressed()
            if keys[pg.K_SPACE]:
                self.init_game()
                self.update()

            pg.display.update()

    def load_screen(self):
        self.finished_loading = False
        start_time = pg.time.get_ticks()
        dots = 0

        while not self.finished_loading:
            # Animate an ellipsis by adding a dot every second
            if pg.time.get_ticks() > start_time + 1000:
                dots += 1
                start_time = pg.time.get_ticks()

            if dots > 3:
                dots = 0

            pg.display.get_surface().fill(pg.Color('black'))
            message = ('  ' * dots) + 'Loading ' + ('. ' * dots) + '    '
            self.display_message(message, self.display_center)

            pg.display.update()
            
           
    def end_screen(self, message):
        game_over = True
        start_time = pg.time.get_ticks()
       
        while game_over:
            # 2 second delay
            if pg.time.get_ticks() > start_time + 2000:
                self.run()

            self.poll_exit()

            pg.display.get_surface().fill(pg.Color('black'))
            self.display_message(message, self.display_center)
            pg.display.update()

    def init_game(self):
        pg.display.get_surface().fill(pg.Color('white'))

        self.current_input = 0
        self.snake.initialize_pos()
        self.apple.spawn()

        # Make one thread to display a loading screen, one to generate a cycle, and poll for events on the main thread
        load = threading.Thread(target=self.load_screen)
        load.start()

        # Find a Hamiltonian cycle around the screen (starting at the snake's starting position) and generate an input list to allow the snake to follow it
        self.graph.init_graph()

        graph_start = int(self.snake.x[0] + self.snake.y[0] / self.snake.side_length)
        cycle = threading.Thread(target=self.graph.hamiltonian_cycle, args=(graph_start,), daemon=True)
        cycle.start()

        # Keep event polling on the main thread, rather than the loading screen, to keep the window responsive
        while cycle.is_alive():
            # Because the loading function depends on pygame, that thread must be terminated before exiting
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.finished_loading = True
                    load.join()
                    pg.quit()
                    sys.exit(0)

        cycle.join()

        # The input list should be generated quickly enough that the window remains responsive
        self.generate_input_list()

        self.finished_loading = True
        load.join()
        
    def check_win_condition(self):
        # The number of squares on the screen
        squares = int((self.display_width / self.snake.side_length) * (self.display_height / self.snake.side_length))

        # Win condition: the snake fills the entire screen
        if self.snake.length >= squares:
            self.end_screen('YOU WIN')

    def update(self):
        while self.snake.dead is False:
            ## INPUT
            self.poll_exit()

            # Set the snake's direction to the current element of the input list
            self.simulate_input()

            ## LOGIC
            self.check_win_condition()
            self.snake.update_position()
            self.check_collision()

            ## RENDER
            self.draw_frame()
            pg.time.Clock().tick(10)
            
        # If the while loop is broken, the snake is dead
        self.end_screen('YOU DIED')
