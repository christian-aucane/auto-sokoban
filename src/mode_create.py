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
        return x == 0 or y == 0 or x == self.width - 1 or y == self.height - 1

    def put_empty_cell(self, x, y):
        if self.cell(x, y) == WALL and self.is_border(x, y):
            return False
        self.set_cell(x, y, EMPTY_CELL)
        return True

    def put_wall(self, x, y):
        self.set_cell(x, y, WALL)
        return True

    def put_goal(self, x, y):
        if self.is_border(x, y):
            return False
        self.set_cell(x, y, GOAL)
        return True

    def put_box(self, x, y):
        if self.is_border(x, y):
            return False
        self.set_cell(x, y, BOX)
        return True
    
    def is_empty(self, x, y):
        return self.cell(x, y) == EMPTY_CELL

    def is_wall(self, x, y):
        return self.cell(x, y) == WALL
    
    def is_goal(self, x, y):
        return self.cell(x, y) == GOAL
    
    def is_box(self, x, y):
        return self.cell(x, y) == BOX
    
    def is_player(self, x, y):
        return self.cell(x, y) == PLAYER
    
    def remove_player(self):
        for i, row in enumerate(self._grid):
            for j, cell in enumerate(row):
                if cell == PLAYER:
                    self.set_cell(j, i, EMPTY_CELL)
                    return True
        return False

    def put_player(self, x, y):
        if self.is_border(x, y):
            return False
        self.remove_player()
        self.set_cell(x, y, PLAYER)
        return True
    
    def sauvegarder_niveau(self, nom_fichier):
        with open(nom_fichier, 'w') as f:
            for ligne in self._grid:
                f.write(''.join(str(element) for element in ligne) + '\n')
