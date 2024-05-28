from copy import deepcopy
from constants import EMPTY_CELL, LEVELS_DIR, WALL, GOAL, UP, DOWN, LEFT, RIGHT


class Entity:
    """
    Entity class
    
    Attributes :
        grid (Grid object) - The grid the entity is on
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
    def __init__(self, grid, x, y):
        """
        Initialize the entity

        Args :
            grid (Grid object) - The grid the entity is on
            x (int) - The x coordinate of the entity
            y (int) - The y coordinate of the entity
        """
        self.grid = grid
        self.x = x
        self.y = y

    @property
    def is_up_available(self):
        """
        Check if the entity can move up

        Returns :
            bool - True if the entity can move up, False otherwise
        """
        return self.y > 0 and not self.grid.is_wall(self.x, self.y - 1)

    @property
    def is_down_available(self):
        """
        Check if the entity can move down

        Returns :
            bool - True if the entity can move down, False otherwise
        """
        return self.y < self.grid.height -1 and not self.grid.is_wall(self.x, self.y + 1)

    @property
    def is_left_available(self):
        """
        Check if the entity can move left

        Returns :
            bool - True if the entity can move left, False otherwise
        """
        return self.x > 0 and not self.grid.is_wall(self.x -1, self.y)

    @property
    def is_right_available(self):
        """
        Check if the entity can move right

        Returns :
            bool - True if the entity can move right, False otherwise
        """
        return self.x < self.grid.width -1 and not self.grid.is_wall(self.x + 1, self.y)

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


class Box(Entity):
    """
    Box class

    Inherited Attributes :
        grid (Grid object) - The grid the box is on
        x (int) - The x coordinate of the box
        y (int) - The y coordinate of the box

    Overriden Properties :
        is_up_available (bool) - True if the box can move up, False otherwise
        is_down_available (bool) - True if the box can move down, False otherwise
        is_left_available (bool) - True if the box can move left, False otherwise
        is_right_available (bool) - True if the box can move right, False otherwise
    
    Properties :
        is_on_goal (bool) - True if the box is on a goal, False otherwise

    Inherited Methods :
        up() - Move the box up
        down() - Move the box down
        left() - Move the box left
        right() - Move the box right

    """
    @property
    def is_up_available(self):
        """
        Check if the box can move up - Override the parent property)

        Returns :
            bool - True if the box can move up, False otherwise
        """
        return super().is_up_available and self.grid.get_box(self.x, self.y - 1) is None

    @property
    def is_down_available(self):
        """
        Check if the box can move down - Override the parent property)

        Returns :
            bool - True if the box can move down, False otherwise
        """
        return super().is_down_available and self.grid.get_box(self.x, self.y + 1) is None

    @property
    def is_left_available(self):
        """
        Check if the box can move left - Override the parent property)

        Returns :
            bool - True if the box can move left, False otherwise
        """
        return super().is_left_available and self.grid.get_box(self.x - 1, self.y) is None

    @property
    def is_right_available(self):
        """
        Check if the box can move right - Override the parent property)

        Returns :
            bool - True if the box can move right, False otherwise
        """
        return super().is_right_available and self.grid.get_box(self.x + 1, self.y) is None
    
    @property
    def is_on_goal(self):
        """
        Check if the box is on a goal

        Returns :
            bool - True if the box is on a goal, False otherwise
        """
        return self.grid.is_goal(self.x, self.y)

class Player(Entity):
    """
    Player class

    Inherited Attributes :
        grid (Grid object) - The grid the player is on
        x (int) - The x coordinate of the player
        y (int) - The y coordinate of the player

    Attributes :
        orientation (int) - The orientation of the player
        
    Inherited Properties :
        is_up_available (bool) - True if the player can move up, False otherwise
        is_down_available (bool) - True if the player can move down, False otherwise
        is_left_available (bool) - True if the player can move left, False otherwise
        is_right_available (bool) - True if the player can move right, False otherwise
        
    Overriden Methods :
        up() - Move the player up
        down() - Move the player down
        left() - Move the player left
        right() - Move the player right
    """
    PLAYER_NOT_MOVED = 0
    PLAYER_MOVED = 1
    BOX_MOVED = 2
    BOX_ON_GOAL = 3

    def __init__(self, grid, x, y, orientation=UP):
        super().__init__(grid, x, y)
        self.orientation = orientation

    def up(self):
        if self.is_up_available:
            box = self.grid.get_box(self.x, self.y - 1)
            if box is not None:
                if box.is_up_available:
                    self.grid.save_backup()
                    box.up()
                    super().up()
                    self.orientation = UP
                    if box.is_on_goal:
                        return self.BOX_ON_GOAL
                    else:
                        return self.BOX_MOVED
                else:
                    return self.PLAYER_NOT_MOVED
            else:
                self.grid.save_backup()
                super().up()
                self.orientation = UP
                return self.PLAYER_MOVED
        else:
            return self.PLAYER_NOT_MOVED

    def down(self):
        if self.is_down_available:
            box = self.grid.get_box(self.x, self.y + 1)
            if box is not None:
                if box.is_down_available:
                    self.grid.save_backup()
                    box.down()
                    super().down()
                    self.orientation = DOWN
                    if box.is_on_goal:
                        return self.BOX_ON_GOAL
                    else:
                        return self.BOX_MOVED
                else:
                    return self.PLAYER_NOT_MOVED
            else:
                self.grid.save_backup()
                super().down()
                self.orientation = DOWN
                return self.PLAYER_MOVED
        else:
            return self.PLAYER_NOT_MOVED
            
    def left(self):
        if self.is_left_available:
            box = self.grid.get_box(self.x - 1, self.y)
            if box is not None:
                if box.is_left_available:
                    
                    self.grid.save_backup()
                    box.left()
                    super().left()
                    self.orientation = LEFT
                    if box.is_on_goal:
                        return self.BOX_ON_GOAL
                    else:
                        return self.BOX_MOVED
                else:
                    return self.PLAYER_NOT_MOVED
            else:
                self.grid.save_backup()
                super().left()
                self.orientation = LEFT
                return self.PLAYER_MOVED
        else:
            return self.PLAYER_NOT_MOVED
            
    def right(self):
        if self.is_right_available:
            box = self.grid.get_box(self.x + 1, self.y)
            if box is not None:
                if box.is_right_available:
                    self.grid.save_backup()
                    box.right()
                    super().right()

                    self.orientation = RIGHT
                    if box.is_on_goal:
                        return self.BOX_ON_GOAL
                    else:
                        return self.BOX_MOVED
                else:
                    return self.PLAYER_NOT_MOVED
            else:
                self.grid.save_backup()
                super().right()
                self.orientation = RIGHT
                return self.PLAYER_MOVED
        else:
            return self.PLAYER_NOT_MOVED


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

    def copy(self):
        return deepcopy(self)
        
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

    @property
    def is_solved(self):
        return all(box.is_on_goal for box in self.boxes)
    
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
        grid = deepcopy(self._grid)
        grid[self.player.y][self.player.x] = "P"
        for box in self.boxes:
            if box.is_on_goal:
                grid[box.y][box.x] = "G"
            else:
                grid[box.y][box.x] = "B"
        for row in grid:
            print(*row, sep=" ")


if __name__ == "__main__":
    grid = Grid(LEVELS_DIR / "grid.txt")
    grid.print()
