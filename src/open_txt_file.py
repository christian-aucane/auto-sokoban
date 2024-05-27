class Grid:
    def __init__(self, txt_path):
        with open(txt_path, "r") as f:
            content = f.readlines()
        self.grid = []
        self.player_x, self.player_y = None, None
        for y, row in enumerate(content):
            row = row.strip()
            new_row = []
            for x, cell in enumerate(row):
                if cell == "4": # player
                    self.player_x, self.player_y = x, y
                    cell = 0
                new_row.append(int(cell))
            self.grid.append(new_row)
    
    def print(self):
        print(*self.grid, sep="\n")
            

if __name__ == "__main__":
    grid = Grid("src/grid/grid1.txt")
    grid.print()
