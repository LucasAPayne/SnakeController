import pygame as pg
from square import Square


class Graph():
    def __init__(self):
        display_width, display_height = pg.display.get_surface().get_size()
        self.row_size = int(display_width / 100)
        self.column_size = int(display_height / 100)
        self.graph = [[0 for x in range(self.row_size * self.row_size)] for y in range(self.row_size * self.row_size)]
        self.path = [-1 for i in range(self.row_size * self.column_size + 1)]

    def init_graph(self):
        for i in range(self.row_size * self.row_size):
            for j in range(i, self.column_size * self.column_size):
                if self.adjacent(i, j):
                    self.graph[i][j] = self.graph[j][i] = 1
                else:
                    self.graph[i][j] = self.graph[j][i] = 0

    def adjacent(self, i, j):
        if j == i + 1 and (i + 1) % self.row_size != 0:
            return True
        elif j == i + self.row_size:
            return True
        else:
            return False

    def is_valid(self, v, k):
        if self.graph[self.path[k - 1]][v] == 0:
            return False

        for i in range(k):
            if self.path[i] == v:
                return False

        return True

    def cycle_found(self, k):
        if k == self.row_size * self.column_size:
            if self.graph[self.path[k - 1]][self.path[0]] == 1:
                return True
            else:
                return False

        for v in range(1, self.row_size * self.column_size):
            if self.is_valid(v, k):
                self.path[k] = v
                if self.cycle_found(k + 1) is True:
                    return True
                self.path[k] = -1

        return False

    def hamiltonian_cycle(self, start):
        self.path[0] = start
        # Initialize to bogus values
        for i in range(1, self.row_size * self.column_size + 1):
            self.path[i] = -1
    
        if self.cycle_found(1) is False:
            return False

        # Since this is a cycle, the last node in the path is the same as the first
        self.path[-1] = self.path[0]

        return True
