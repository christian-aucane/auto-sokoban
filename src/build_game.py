from game.base_grid import BaseGrid
from game.entities import Box, Player
from constants import BOX, LEVELS_DIR, PLAYER

class Level(BaseGrid):
    # TODO : add docstrings
    def __init__(self, grid_content, name=None):
        self.content = grid_content
        self.name = name
        self.reset_count = 0
        self.solve_used = False
            
        self.boxes = []
        self.player = None
        grid = self.load()
        super().__init__(grid)

        self.backup = {"boxes": self.boxes, "player": self.player}
        self.backup_saved = False
        self._moves_count = 0

    @classmethod
    def from_file(cls, txt_path):
        with open(txt_path, "r") as f:
            content = f.readlines()
        name = txt_path.stem  # Extract the file name without extension
        return cls(content, name)

    def is_player(self, x, y):
        return self.player.x == x and self.player.y == y
    
    def is_box( self, x, y):
        return self.get_box(x, y) is not None

    def save_backup(self):
        # TODO : Ajouter des methodes copy aux objets
        self.backup["boxes"] = [Box(self, box.x, box.y) for box in self.boxes]
        self.backup["player"] = Player(self, self.player.x, self.player.y, self.player.orientation)
        self.backup_saved = True

    def load(self, content=None):
        if content is None:
            content = self.content
        grid = []
        for y, row in enumerate(content):
            row = row.strip()
            new_row = []
            for x, cell in enumerate(row):
                cell = int(cell)
                if cell == BOX:
                    self.boxes.append(Box(self, x, y))
                    cell = 0
                if cell == PLAYER:
                    if self.player is not None:
                        raise ValueError("Multiple players")
                    self.player = Player(self, x, y)
                    cell = 0
                new_row.append(cell)
            grid.append(new_row)
        
        self._moves_count = 0
        return grid

    def reset(self):
        self.boxes = []
        self.player = None
        self.grid = self.load()
        self.reset_count += 1  # Increment the reset count

    def cancel(self):
        if self.backup_saved:
            self.boxes = self.backup["boxes"]
            self.player = self.backup["player"]
            self._moves_count -= 1
            self.backup_saved = False
            return True
        return False

    def add_move(self):
        self._moves_count += 1

    def load_solve(self):
        self.solve_used = True

    @property
    def moves_count(self):
        return self._moves_count
    
    @moves_count.setter
    def moves_count(self, value):
        raise AttributeError("Cannot set moves_count directly")

    @property
    def is_solved(self):
        return all(box.is_on_goal for box in self.boxes)

    @property
    def boxes_on_goal(self):
        return sum(box.is_on_goal for box in self.boxes)

    def get_box(self, x, y):
        for box in self.boxes:
            if box.x == x and box.y == y:
                return box
        return None
    
    @property
    def counter(self):
        counter = super().counter
        counter["boxes"] = len(self.boxes)
        counter["player"] = 1 if self.player is not None else 0
        counter["boxes_on_goal"] = self.boxes_on_goal
        return counter
    

if __name__ == "__main__":
    grid = Level.from_file(LEVELS_DIR / "grid.txt")
    grid.print()
