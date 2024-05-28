from pathlib import Path
# TODO : Utiliser des classes pour séparer les constantes

# Entities
EMPTY_CELL = 0
WALL = 1
GOAL = 2

# Player orientation
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

# Pages
HOME = 0
LEVEL = 1
CREATE = 2
PLAYERS = 3
RANKING = 4

WIDTH, HEIGHT = 600, 600
LEVEL_MENU_HEIGHT = 100

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Paths
IMAGES_DIR = Path(__file__).parent / "images"
LEVELS_DIR = Path(__file__).parent / "levels"
