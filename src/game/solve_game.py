from collections import deque

from build_game import Level, Player
from constants import Orientations, Paths


# TODO : remove prints

class LevelSolver:
    """
    Solve the game
    
    Attributes:
        level: Grid object
        original_level: Grid object
        solution: list of moves

    Methods:
        solve(self) : Solve the game
        get_state(self) : Get the current state of the level
        set_state(self, state) : Set the state of the level
        get_next_move(self) : Get the next move from the solution
        apply_move(self, state, move) : Apply the move to the level
        apply_next_move(self) : Apply the next move from the solution
        possible_moves(self) : Get the possible moves from the level
    """
    # Breadth-First Search
    def __init__(self, level):
        """
        Initialize the solver with the initial level

        Args:
            level: Grid object
        """
        self.original_level = level
        self.level = level.copy()
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
            if self.level.is_solved:
                self.solution = path
                print("SOLVING MOVES : ", self.level.moves_count)
                self.level = self.original_level  # Restore the original level
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
        Get the current state of the level
        
        Returns:
            tuple: current state
        """
        boxes = tuple((box.x, box.y) for box in self.level.boxes)
        player = (self.level.player.x, self.level.player.y)
        return (player, boxes)

    def set_state(self, state):
        """
        Set the state of the level
        
        Args:
            state: state to set
        """
        player, boxes = state
        self.level.player.x, self.level.player.y = player
        for i, (x, y) in enumerate(boxes):
            self.level.boxes[i].x, self.level.boxes[i].y = x, y

    def possible_moves(self):
        """
        Get the possible moves from the level
        
        Returns:
            list: list of possible moves
        """
        moves = []
        directions = [
            (Orientations.UP, self.level.player.up),
            (Orientations.DOWN, self.level.player.down),
            (Orientations.LEFT, self.level.player.left),
            (Orientations.RIGHT, self.level.player.right)
        ]
        for direction, move in directions:
            if move() != Player.PLAYER_NOT_MOVED:
                moves.append(direction)
                self.level.cancel()  # Revert move to check other directions
        return moves

    def apply_move(self, state, move):
        """
        Apply the move to the level

        Args:
            state: state to apply the move
            move: move to apply

        Returns:
            tuple: new state
        """
        self.set_state(state)
        if move == Orientations.UP:
            self.level.player.up()
        elif move == Orientations.DOWN:
            self.level.player.down()
        elif move == Orientations.LEFT:
            self.level.player.left()
        elif move == Orientations.RIGHT:
            self.level.player.right()
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
    level = Level.from_file(Paths.LEVELS / "grid.txt")
    solver = LevelSolver(level)
    is_solved = solver.solve()
    print("IS SOLVED", is_solved)
    if not is_solved:
        print("NO SOLUTION FOUND")
        exit()
    print("SOLUTION", solver.solution)
    while True:
        if solver.apply_next_move():
            print("MOVING")
            level.print()

        elif level.is_solved:
            print("SOLUTION FOUND")
            break
