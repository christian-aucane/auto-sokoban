from collections import deque

from build_game import Grid, Player
from constants import LEVELS_DIR, UP, DOWN, LEFT, RIGHT


class Solver:
    # Breadth-First Search
    def __init__(self, grid):
        """
        Initialize the solver with the initial grid

        Args:
            grid: Grid object
        """
        self.original_grid = grid
        self.grid = grid.copy()
        self.solution = []

    def solve(self):
        """
        Solve the game and return True if a solution is found, False otherwise

        Returns:
            bool: True if a solution is found, False otherwise
        """
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
        """
        Get the next move from the solution
        
        Returns:
            tuple: next move
        """
        if self.solution:
            return self.solution.pop(0)
        return None

    def get_state(self):
        """
        Get the current state of the grid
        
        Returns:
            tuple: current state
        """
        boxes = tuple((box.x, box.y) for box in self.grid.boxes)
        player = (self.grid.player.x, self.grid.player.y)
        return (player, boxes)

    def set_state(self, state):
        """
        Set the state of the grid
        
        Args:
            state: state to set
        """
        player, boxes = state
        self.grid.player.x, self.grid.player.y = player
        for i, (x, y) in enumerate(boxes):
            self.grid.boxes[i].x, self.grid.boxes[i].y = x, y

    def possible_moves(self):
        """
        Get the possible moves from the grid
        
        Returns:
            list: list of possible moves
        """
        moves = []
        directions = [(UP, self.grid.player.up), (DOWN, self.grid.player.down),
                      (LEFT, self.grid.player.left), (RIGHT, self.grid.player.right)]
        for direction, move in directions:
            if move() != Player.PLAYER_NOT_MOVED:
                moves.append(direction)
                self.grid.cancel()  # Revert move to check other directions
        return moves

    def apply_move(self, state, move):
        """
        Apply the move to the grid

        Args:
            state: state to apply the move
            move: move to apply

        Returns:
            tuple: new state
        """
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
    
    def apply_next_move(self):
        """
        Apply the next move from the solution

        Returns:
            bool: True if the move was applied, False otherwise
        """
        next_move = self.get_next_move()
        if next_move is not None:
            next_state = self.apply_move(self.get_state(), next_move)
            self.set_state(next_state)
            return True
        return False
    

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
        if solver.apply_next_move():
            print("MOVING")
            # Afficher la grille mise à jour (vous pouvez ajouter cette fonction à votre classe SokobanApp)
            grid.print()

        elif grid.is_solved:
            print("SOLUTION FOUND")
            break
