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

        self._current_tool = EMPTY_CELL
        
    @property
    def current_tool(self):
        mapping = {EMPTY_CELL: "empty", WALL: "wall", GOAL: "goal", BOX: "box", PLAYER: "player"}
        return mapping[self._current_tool]
    
    @current_tool.setter
    def current_tool(self, value):
        mapping = {"empty": EMPTY_CELL, "wall": WALL, "goal": GOAL, "box": BOX, "player": PLAYER}
        self._current_tool = mapping[value]

    def put(self, x, y):
        if self._current_tool == EMPTY_CELL:
            return self.put_empty_cell(x, y)
        if self._current_tool == WALL:
            return self.put_wall(x, y)
        if self._current_tool == GOAL:
            return self.put_goal(x, y)
        if self._current_tool == BOX:
            return self.put_box(x, y)
        if self._current_tool == PLAYER:
            return self.put_player(x, y)
        return False

    def set_cell(self, x, y, value):
        print("BEFORE : ", *self._grid, sep="\n", end="\n\n")
        self._grid[y][x] = value
        
        print("AFTER : ", *self._grid, sep="\n", end="\n\n")

    def cell(self, x, y):
        return self._grid[y][x]

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
    
    def put_player(self, x, y):
        if self.is_border(x, y):
            return False
        self.remove_player()
        self.set_cell(x, y, PLAYER)
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
        for y in range(self.height):
            for x in range(self.width):
                if self.is_player(x, y):
                    self.set_cell(x, y, EMPTY_CELL)
                    return True
        return False
    
    def save(self, filename):
        with open(filename, 'w') as f:
            for row in self._grid:
                f.write(''.join(str(cell) for cell in row) + '\n')

    @property
    def counter(self):
        # TODO : utiliser un default_dict
        counter = {"empty": 0, "wall": 0, "goal": 0, "box": 0, "player": 0}
        for y in range(self.height):
            for x in range(self.width):
                if self.is_empty(x, y):
                    counter["empty"] += 1
                if self.is_wall(x, y):
                    counter["wall"] += 1
                if self.is_goal(x, y):
                    counter["goal"] += 1
                if self.is_box(x, y):
                    counter["box"] += 1
                if self.is_player(x, y):
                    counter["player"] += 1
        return counter
