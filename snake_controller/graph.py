import pygame as pg

from entities.square import Square

class Graph():
    def __init__(self):
        display_width, display_height = pg.display.get_surface().get_size()
        node = Square(0, 0, pg.Color('black'))

        self.row_size = int(display_width / node.side_length)
        self.column_size = int(display_height / node.side_length)

        # Initialize adjacency matrix to all 0s, indicating no connections
        self.graph = [[0 for x in range(self.row_size * self.row_size)] for y in range(self.row_size * self.row_size)]

        # Initialize cycle to bogus values, and add an extra element to make it repeatable
        self.cycle = [-1 for i in range(self.row_size * self.column_size + 1)]

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
        if self.graph[self.cycle[k - 1]][v] == 0:
            return False

        for i in range(k):
            if self.cycle[i] == v:
                return False

        return True

    def cycle_found(self, k):
        if k == self.row_size * self.column_size:
            if self.graph[self.cycle[k - 1]][self.cycle[0]] == 1:
                return True
            else:
                return False

        for v in range(1, self.row_size * self.column_size):
            if self.is_valid(v, k):
                self.cycle[k] = v
                if self.cycle_found(k + 1) is True:
                    return True
                self.cycle[k] = -1

        return False

    def hamiltonian_cycle(self, start):
        self.cycle[0] = start
    
        if self.cycle_found(1) is False:
            return False

        # Since this is a cycle, the last node is the same as the first
        self.cycle[-1] = self.cycle[0]
        
        return True
