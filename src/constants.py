from enum import Enum, auto
from pathlib import Path

import pygame
from pygame.font import Font


class CellsValues:
    EMPTY_CELL = 0
    WALL = 1
    GOAL = 2
    BOX = 3
    PLAYER = 4


class Orientations(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class Sizes:
    GRID_WIDTH, GRID_HEIGHT = 600, 600
    MENU_HEIGHT = 100
    WIDTH, HEIGHT = GRID_WIDTH, GRID_HEIGHT + MENU_HEIGHT
    MENU_BUTTON_HEIGHT = MENU_HEIGHT // 2
    MAIN_MENU_BUTTON_WIDTH = 200
    MAIN_MENU_BUTTON_HEIGHT = 50
    MAIN_MENU_SLIDER_WIDTH = GRID_WIDTH - 200
    MAIN_MENU_SLIDER_HEIGHT = 20
    FONT = 30
    SCORE_FONT = 20


class Colors:
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)

    BUTTON_TEXT = BLACK
    BUTTON_HOVER_TEXT = RED
    BUTTON_ACTIVE_TEXT = BLUE

    ERROR = RED

    SLIDER_BG = BLACK
    SLIDER = WHITE
    SLIDER_KNOB = RED
    SLIDER_TEXT = BLACK


class Paths:
    SOURCE = Path(__file__).parent
    ASSETS = SOURCE / "assets"
    IMAGES = ASSETS / "images"
    MUSIC = ASSETS / "music"
    SOUND_EFFECTS = ASSETS / "sound_effects"
    LEVELS = SOURCE / "levels"
    CUSTOM_LEVELS = SOURCE / "custom_levels"
    FONT = ASSETS / "font" / "font.ttf"
    BUTTONS_IMAGES = IMAGES / "buttons"
    CELLS_IMAGES = IMAGES / "cells"
    BACKGROUND_IMAGES = IMAGES / "backgrounds"

    MAIN_MENU_BUTTON = BUTTONS_IMAGES / "main_menu.png"
    MENU_BUTTON = BUTTONS_IMAGES / "menu.png"
    DELETE_BUTTON = BUTTONS_IMAGES / "delete.png"

    SCORES_FILE = SOURCE / "scores.csv"


# Max
MAX_CUSTOM_LEVELS = 3

# Pos
MAIN_MENU_BUTTONS_X = Sizes.WIDTH // 2 - Sizes.MAIN_MENU_BUTTON_WIDTH // 2
MAIN_MENU_SLIDERS_X = Sizes.WIDTH // 2 - Sizes.MAIN_MENU_SLIDER_WIDTH // 2

# Font
pygame.font.init()
FONT = Font(Paths.FONT, Sizes.FONT)

# TODO : modifier la font des boutons
BUTTON_FONT = Font(Paths.FONT, Sizes.FONT)

SCORE_FONT = Font(Paths.FONT, Sizes.SCORE_FONT)

OFFSET = 15

MAX_PLAYER_NAME_CHARS = 8
MAX_SCORES_DISPLAYED = 15