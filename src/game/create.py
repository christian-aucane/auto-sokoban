from build_game import Level
from .solve import LevelSolver
from .base import BaseGrid
from constants import CellsValues


class LevelCreator(BaseGrid):
    def __init__(self, width, height):
        grid = [[CellsValues.EMPTY_CELL for _ in range(
            width)] for _ in range(height)]
        for i in range(width):
            grid[0][i] = CellsValues.WALL
            grid[height-1][i] = CellsValues.WALL
        for i in range(height):
            grid[i][0] = CellsValues.WALL
            grid[i][width-1] = CellsValues.WALL
        super().__init__(grid)
        self._current_tool = CellsValues.EMPTY_CELL

    @classmethod
    def from_file(cls, txt_path):
        with open(txt_path, "r") as f:
            content = f.readlines()
            obj = cls(len(content[0].strip()), len(content))
        obj.grid = [[int(cell) for cell in row.strip()] for row in content]
        return obj
        
    @property
    def current_tool(self):
        mapping = {
            CellsValues.EMPTY_CELL: "empty",
            CellsValues.WALL: "wall",
            CellsValues.GOAL: "goal",
            CellsValues.BOX: "box",
            CellsValues.PLAYER: "player"
        }
        return mapping[self._current_tool]
    
    @current_tool.setter
    def current_tool(self, value):
        mapping = {
            "empty": CellsValues.EMPTY_CELL,
            "wall": CellsValues.WALL,
            "goal": CellsValues.GOAL,
            "box": CellsValues.BOX,
            "player": CellsValues.PLAYER
        }
        self._current_tool = mapping[value]

    def put(self, x, y):
        if self._current_tool == CellsValues.EMPTY_CELL:
            return self.put_empty_cell(x, y)
        if self._current_tool == CellsValues.WALL:
            return self.put_wall(x, y)
        if self._current_tool == CellsValues.GOAL:
            return self.put_goal(x, y)
        if self._current_tool == CellsValues.BOX:
            return self.put_box(x, y)
        if self._current_tool == CellsValues.PLAYER:
            return self.put_player(x, y)
        return False

    def is_border(self, x, y):
        return x == 0 or y == 0 or x == self.width - 1 or y == self.height - 1

    def put_empty_cell(self, x, y):
        if self.get_cell(x, y) == CellsValues.WALL and self.is_border(x, y):
            return False
        self.set_cell(x, y, CellsValues.EMPTY_CELL)
        return True

    def put_wall(self, x, y):
        self.set_cell(x, y, CellsValues.WALL)
        return True

    def put_goal(self, x, y):
        if self.is_border(x, y):
            return False
        self.set_cell(x, y, CellsValues.GOAL)
        return True

    def put_box(self, x, y):
        if self.is_border(x, y):
            return False
        self.set_cell(x, y, CellsValues.BOX)
        return True
    
    def put_player(self, x, y):
        if self.is_border(x, y):
            return False
        self.remove_player()
        self.set_cell(x, y, CellsValues.PLAYER)
        return True
    
    def remove_player(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.is_player(x, y):
                    self.set_cell(x, y, CellsValues.EMPTY_CELL)
                    return True
        return False
    
    def save(self, filename):
        with open(filename, 'w') as f:
            for row in self.grid:
                f.write(''.join(str(cell) for cell in row) + '\n')
                
    def is_complete(self):
        counter = self.counter
        content = ["".join(map(str, row)) for row in self.grid]
        level = Level(content)
        solver = LevelSolver(level)
        if counter["box"] != counter["goal"]\
            or not counter["player"]\
                or not counter["box"]:
            return False
        if not solver.solve():
            return False
        return True
