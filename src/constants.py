from pathlib import Path

# Entities
EMPTY_CELL = 0
WALL = 1
GOAL = 2

# Player orientation
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

WIDTH, HEIGHT = 600, 600

# Colors
WHITE = (255, 255, 255)

IMAGES_DIR = Path(__file__).parent / "images"
