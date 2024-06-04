from copy import deepcopy

import numpy as np

from constants import CellsValues


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
    
    def get_cell(self, x, y):
        return self._grid[y, x]
    
    def set_cell(self, x, y, value):
        self._grid[y, x] = value

    def is_empty(self, x, y):
        return self.get_cell(x, y) == CellsValues.EMPTY_CELL
    
    def is_wall(self, x, y):
        return self.get_cell(x, y) == CellsValues.WALL
    
    def is_goal(self, x, y):
        return self.get_cell(x, y) == CellsValues.GOAL
    
    def is_player(self, x, y):
        return self.get_cell(x, y) == CellsValues.PLAYER
    
    def is_box(self, x, y):
        return self.get_cell(x, y) == CellsValues.BOX
    
    @property
    def counter(self):
        return {
            "empty": np.sum(self._grid == CellsValues.EMPTY_CELL),
            "wall": np.sum(self._grid == CellsValues.WALL),
            "goal": np.sum(self._grid == CellsValues.GOAL),
            "box": np.sum(self._grid == CellsValues.BOX),
            "player": np.sum(self._grid == CellsValues.PLAYER),
        }

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
