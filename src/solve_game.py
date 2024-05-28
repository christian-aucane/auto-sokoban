from collections import deque

from build_game import Grid, Player
from constants import LEVELS_DIR, UP, DOWN, LEFT, RIGHT


class Solver:
    def __init__(self, grid):
        self.original_grid = grid
        self.grid = grid.copy()
        self.solution = []

    def solve(self):
        initial_state = self.get_state()
        queue = deque([(initial_state, [])])
        visited = set()
        visited.add(initial_state)

        while queue:
            current_state, path = queue.popleft()
            self.set_state(current_state)
            if self.grid.is_solved:
                self.solution = path
                self.grid = self.original_grid
                return True

            for move in self.possible_moves():
                next_state = self.apply_move(current_state, move)
                if next_state not in visited:
                    visited.add(next_state)
                    queue.append((next_state, path + [move]))

        self.solution = None  # No solution found
        return False

    def get_next_move(self):
        if self.solution:
            return self.solution.pop(0)
        return None

    def get_state(self):
        boxes = tuple((box.x, box.y) for box in self.grid.boxes)
        player = (self.grid.player.x, self.grid.player.y)
        return (player, boxes)

    def set_state(self, state):
        player, boxes = state
        self.grid.player.x, self.grid.player.y = player
        for i, (x, y) in enumerate(boxes):
            self.grid.boxes[i].x, self.grid.boxes[i].y = x, y

    def possible_moves(self):
        moves = []
        directions = [(UP, self.grid.player.up), (DOWN, self.grid.player.down),
                      (LEFT, self.grid.player.left), (RIGHT, self.grid.player.right)]
        for direction, move in directions:
            if move() != Player.PLAYER_NOT_MOVED:
                moves.append(direction)
                self.grid.cancel()  # Revert move to check other directions
        return moves

    def apply_move(self, state, move):
        self.set_state(state)
        if move == UP:
            self.grid.player.up()
        elif move == DOWN:
            self.grid.player.down()
        elif move == LEFT:
            self.grid.player.left()
        elif move == RIGHT:
            self.grid.player.right()
        return self.get_state()
    

if __name__ == "__main__":
    grid = Grid(LEVELS_DIR / "grid.txt")
    solver = Solver(grid)
    is_solved = solver.solve()
    print("IS SOLVED", is_solved)
    if not is_solved:
        print("NO SOLUTION FOUND")
        exit()
    print("SOLUTION", solver.solution)
    while True:
        next_move = solver.get_next_move()
        if next_move is not None:
            print(f"Next move: {next_move}")
            # Appliquer le mouvement à la grille en utilisant apply_move()
            next_state = solver.apply_move(solver.get_state(), next_move)
            solver.set_state(next_state)

            # Afficher la grille mise à jour (vous pouvez ajouter cette fonction à votre classe SokobanApp)
            grid.print()

        elif grid.is_solved:
            print("SOLUTION FOUND")
            break
        else:
            print("SOLUTION NOT FOUND")
            break
