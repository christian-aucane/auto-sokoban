from pathlib import Path
# TODO : Utiliser des classes pour séparer les constantes

# Entities
EMPTY_CELL = 0
WALL = 1
GOAL = 2
BOX = 3
PLAYER = 4

# Player orientation
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

# Pages
HOME = 0
LEVEL = 1
CREATE = 2

# Sizes
GRID_WIDTH, GRID_HEIGHT = 600, 600
MENU_HEIGHT = 100
WIDTH, HEIGHT = GRID_WIDTH, GRID_HEIGHT + MENU_HEIGHT
MENU_BUTTON_HEIGHT = MENU_HEIGHT // 2

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Paths
SOURCES_DIR = Path(__file__).parent
ASSETS_DIR = SOURCES_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
MUSIC_DIR = ASSETS_DIR / "music"
SOUND_EFFECTS_DIR = ASSETS_DIR / "sound_effects"
LEVELS_DIR = SOURCES_DIR / "levels"
CUSTOM_LEVELS_DIR = SOURCES_DIR / "custom_levels"
