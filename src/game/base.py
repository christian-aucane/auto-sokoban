from copy import deepcopy

import numpy as np

from constants import CellsValues, Orientations


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
        print(
            *[
                " ".join(
                    str(cell.decode("utf-8")) for cell in row
                ) for row in grid
            ],
            sep="\n"
        )


class BaseEntity:
    """
    Base class for the entities
    
    Attributes :
        level (Level object) - The level the entity is on
        x (int) - The x coordinate of the entity
        y (int) - The y coordinate of the entity

    Properties :
        is_up_available (bool) - True if the entity can move up, False otherwise
        is_down_available (bool) - True if the entity can move down, False otherwise
        is_left_available (bool) - True if the entity can move left, False otherwise
        is_right_available (bool) - True if the entity can move right, False otherwise

    Methods :
        up() - Move the entity up
        down() - Move the entity down
        left() - Move the entity left
        right() - Move the entity right
    """
    def __init__(self, level, x, y):
        """
        Initialize the entity

        Args :
            grid (Grid object) - The grid the entity is on
            x (int) - The x coordinate of the entity
            y (int) - The y coordinate of the entity
        """
        self.level = level
        self.x = x
        self.y = y

    @property
    def is_up_available(self):
        """
        Check if the entity can move up

        Returns :
            bool - True if the entity can move up, False otherwise
        """
        return self.y > 0 and not self.level.is_wall(self.x, self.y - 1)

    @property
    def is_down_available(self):
        """
        Check if the entity can move down

        Returns :
            bool - True if the entity can move down, False otherwise
        """
        return self.y < self.level.height -1\
            and not self.level.is_wall(self.x, self.y + 1)

    @property
    def is_left_available(self):
        """
        Check if the entity can move left

        Returns :
            bool - True if the entity can move left, False otherwise
        """
        return self.x > 0 and not self.level.is_wall(self.x -1, self.y)

    @property
    def is_right_available(self):
        """
        Check if the entity can move right

        Returns :
            bool - True if the entity can move right, False otherwise
        """
        return self.x < self.level.width -1\
            and not self.level.is_wall(self.x + 1, self.y)

    def up(self):
        """
        Move the entity up

        Returns :
            bool - True if the entity moved up, False otherwise
        """
        if self.is_up_available:
            self.y -= 1
            return True
        return False

    def down(self):
        """
        Move the entity down

        Returns :
            bool - True if the entity moved down, False otherwise
        """
        if self.is_down_available:
            self.y += 1
            return True
        return False

    def left(self):
        """
        Move the entity left

        Returns :
            bool - True if the entity moved left, False otherwise
        """
        if self.is_left_available:
            self.x -= 1
            return True
        return False

    def right(self):
        """
        Move the entity right

        Returns :
            bool - True if the entity moved right, False otherwise
        """
        if self.is_right_available:
            self.x += 1
            return True
        return False

    def move(self, direction):
        """
        Move the entity in the specified direction

        Args :
            direction (int) - The direction to move the entity in

        Returns :
            bool - True if the entity moved in the specified direction, False otherwise
        """
        if direction == Orientations.UP:
            return self.up()
        elif direction == Orientations.DOWN:
            return self.down()
        elif direction == Orientations.LEFT:
            return self.left()
        elif direction == Orientations.RIGHT:
            return self.right()
        
    def copy(self):
        """
        Copy the entity

        Returns :
            Entity object - The copy of the entity
        """
        return self.__class__(**self.__dict__)
