from constants import EMPTY_CELL, WALL, GOAL, BOX, PLAYER


class Create:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._grid = [[EMPTY_CELL for _ in range(
            width)] for _ in range(height)]
        for i in range(width):
            self._grid[0][i] = WALL
            self._grid[height-1][i] = WALL
        for i in range(height):
            self._grid[i][0] = WALL
            self._grid[i][width-1] = WALL

    def set_cell(self, x, y, value):
        self._grid[x][y] = value

    def cell(self, x, y):
        return self._grid[x][y]

    def is_border(self, x, y):
        return all([x != 0, y != 0, x != self.width - 1, y != self.height - 1])

    def put_empty_cell(self, x, y):
        if self.cell(x, y) == WALL and self.is_border(x, y):
            return False
        self.set_cell(x, y, EMPTY_CELL)
        return True

    def put_wall(self, x, y):
        self.set_cell(x, y, WALL)
        return True

    