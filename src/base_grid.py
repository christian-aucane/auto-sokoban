from copy import deepcopy
import numpy as np

from constants import BOX, EMPTY_CELL, GOAL, PLAYER, WALL


class BaseGrid:

    def __init__(self, grid):
        self._grid = np.array(grid)
    
    @property
    def grid(self):
        return self._grid.tolist()
    
    @grid.setter
    def grid(self, grid):
        self._grid = np.array(grid)

    @property
    def width(self):
        return self._grid.shape[1]
    
    @property
    def height(self):
        return self._grid.shape[0]
    
    def copy(self):
        return deepcopy(self)
    
    def cell(self, x, y):
        return self._grid[y, x]
    
    def is_empty(self, x, y):
        return self.cell(x, y) == EMPTY_CELL
    
    def is_wall(self, x, y):
        return self.cell(x, y) == WALL
    
    def is_goal(self, x, y):
        return self.cell(x, y) == GOAL
    
    def is_player(self, x, y):
        return self.cell(x, y) == PLAYER
    
    def is_box(self, x, y):
        return self.cell(x, y) == BOX
    
    def print(self):
        grid = np.chararray((self.height, self.width))
        for y in range(self.height):
            for x in range(self.width):
                if self.is_goal(x, y):
                    grid[y, x] = "G"
                if self.is_wall(x, y):
                    grid[y, x] = "W"
                if self.is_empty(x, y):
                    grid[y, x] = "_"
                if self.is_player(x, y):
                    grid[y, x] = "P"
                if self.is_box(x, y):
                    grid[y, x] = "B"
        print(*[" ".join(str(cell.decode("utf-8")) for cell in row) for row in grid], sep="\n")
