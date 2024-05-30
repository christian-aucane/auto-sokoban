from base_grid import BaseGrid
from constants import BOX, LEVELS_DIR, PLAYER
from entities import Box, Player


class Level(BaseGrid):
    # TODO : add docstrings
    def __init__(self, txt_path):
        with open(txt_path, "r") as f:
            self.content = f.readlines()
            
        self.boxes = []
        self.player = None
        grid = self.load(self.content)
        
        super().__init__(grid)

        self.backup = {"boxes": self.boxes, "player": self.player}
        self.backup_saved = False

    def is_player(self, x, y):
        return self.player.x == x and self.player.y == y
    
    def is_box( self, x, y):
        if self.get_box(x, y) is None:
            return False
        return True

    def save_backup(self):
        # TODO : Ajouter des methodes copy aux objets
        self.backup["boxes"] = [Box(self, box.x, box.y) for box in self.boxes]
        self.backup["player"] = Player(self, self.player.x, self.player.y, self.player.orientation)
        self.backup_saved = True

    def load(self, content=None):
        # TODO : ajouter vérifiction sur la forme de la matrice
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
        return grid

    def reset(self):
        self.boxes = []
        self.player = None
        self.grid = self.load(self.content)

    def cancel(self):
        if self.backup_saved:
            self.boxes = self.backup["boxes"]
            self.player = self.backup["player"]
            return True
        return False

    @property
    def is_solved(self):
        return all(box.is_on_goal for box in self.boxes)

    def get_box(self, x, y):
        for box in self.boxes:
            if box.x == x and box.y == y:
                return box
        return None
    

if __name__ == "__main__":
    grid = Level(LEVELS_DIR / "grid.txt")
    grid.print()
