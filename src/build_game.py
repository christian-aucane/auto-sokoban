from copy import deepcopy
from constants import EMPTY_CELL, WALL, GOAL, UP, DOWN, LEFT, RIGHT


class Entity:
    def __init__(self, grid, x, y):
        self.grid = grid
        self.x = x
        self.y = y

    @property
    def is_up_available(self):
        return self.y > 0 and not self.grid.is_wall(self.x, self.y - 1)

    @property
    def is_down_available(self):
        return self.y < self.grid.height -1 and not self.grid.is_wall(self.x, self.y + 1)

    @property
    def is_left_available(self):
        return self.x > 0 and not self.grid.is_wall(self.x -1, self.y)

    @property
    def is_right_available(self):
        return self.x < self.grid.width -1 and not self.grid.is_wall(self.x + 1, self.y)

    def up(self):
        if self.is_up_available:
            self.y -= 1
            return True
        return False

    def down(self):
        if self.is_down_available:
            self.y += 1
            return True
        return False

    def left(self):
        if self.is_left_available:
            self.x -= 1
            return True
        return False

    def right(self):
        if self.is_right_available:
            self.x += 1
            return True
        return False


class Box(Entity):
    @property
    def is_up_available(self):
        return super().is_up_available and self.grid.get_box(self.x, self.y - 1) is None

    @property
    def is_down_available(self):
        return super().is_down_available and self.grid.get_box(self.x, self.y + 1) is None

    @property
    def is_left_available(self):
        return super().is_left_available and self.grid.get_box(self.x - 1, self.y) is None

    @property
    def is_right_available(self):
        return super().is_right_available and self.grid.get_box(self.x + 1, self.y) is None
    
    @property
    def is_on_goal(self):
        return self.grid.is_goal(self.x, self.y)

class Player(Entity):
    def __init__(self, grid, x, y, orientation=UP):
        super().__init__(grid, x, y)
        self.orientation = orientation

    def up(self):
        self.grid.save_backup()
        if self.is_up_available:
            box = self.grid.get_box(self.x, self.y - 1)
            if box is not None:
                if box.is_up_available:
                    box.up()
                    super().up()
                    self.orientation = UP
                    return True
                else:
                    return False
            else:
                super().up()
                self.orientation = UP
                return True
        else:
            return False

    def down(self):
        if self.is_down_available:
            box = self.grid.get_box(self.x, self.y + 1)
            if box is not None:
                if box.is_down_available:
                    self.grid.save_backup()
                    box.down()
                    super().down()
                    self.orientation = DOWN
                    return True
                else:
                    return False
            else:
                self.grid.save_backup()
                super().down()
                self.orientation = DOWN
                return True
            
    def left(self):
        if self.is_left_available:
            box = self.grid.get_box(self.x - 1, self.y)
            if box is not None:
                if box.is_left_available:
                    
                    self.grid.save_backup()
                    box.left()
                    super().left()
                    self.orientation = LEFT
                    return True
                else:
                    return False
            else:
                self.grid.save_backup()
                super().left()
                self.orientation = LEFT
                return True
            
    def right(self):
        if self.is_right_available:
            box = self.grid.get_box(self.x + 1, self.y)
            if box is not None:
                if box.is_right_available:
                    self.grid.save_backup()
                    box.right()
                    super().right()

                    self.orientation = RIGHT
                    return True
                else:
                    return False
            else:
                self.grid.save_backup()
                super().right()
                self.orientation = RIGHT
                return True


class Grid:
    def __init__(self, txt_path):
        with open(txt_path, "r") as f:
            self.content = f.readlines()
            
        self._grid = []
        self.boxes = []
        self.player = None

        self.backup = {"boxes": self.boxes, "player": self.player}
        self.backup_saved = False

        self.load()
        
    def save_backup(self):
        # TODO : Ajouter des methodes copy aux objets
        self.backup["boxes"] = [Box(self, box.x, box.y) for box in self.boxes]
        self.backup["player"] = Player(self, self.player.x, self.player.y, self.player.orientation)
        self.backup_saved = True

    def load(self):
        # TODO : ajouter vérifiction sur la forme de la matrice
        for y, row in enumerate(self.content):
            row = row.strip()
            new_row = []
            for x, cell in enumerate(row):
                if cell == "3":  # box
                    self.boxes.append(Box(self, x, y))
                    cell = 0
                if cell == "4":  # player
                    if self.player is not None:
                        raise ValueError("Multiple players")
                    self.player = Player(self, x, y)
                    cell = 0
                new_row.append(int(cell))
            self._grid.append(new_row)

        self._width = len(self._grid[0])
        self._height = len(self._grid)

    def reset(self):
        self._grid = []
        self.boxes = []
        self.player = None
        self.load()

    def cancel(self):
        if self.backup_saved:
            self.boxes = self.backup["boxes"]
            self.player = self.backup["player"]
            return True
        return False

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        raise ValueError("Cannot change width")
    
    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, value):
        raise ValueError("Cannot change height")

    def cell(self, x, y):
        return self._grid[y][x]
    
    def is_empty(self, x, y):
        return self.cell(x, y) == EMPTY_CELL

    def is_wall(self, x, y):
        return self.cell(x, y) == WALL
    
    def is_goal(self, x, y):
        return self.cell(x, y) == GOAL

    def get_box(self, x, y):
        for box in self.boxes:
            if box.x == x and box.y == y:
                return box
        return None
    
    def print(self):
        print(*self._grid, sep="\n")


if __name__ == "__main__":
    grid = Grid("src/grid/grid1.txt")
    grid.print()
