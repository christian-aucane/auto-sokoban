import pygame

from screens.base import BaseScreen
from widgets import Button
from constants import WIDTH, GREEN, RED, BLACK, HEIGHT, GRID_WIDTH, GRID_HEIGHT, IMAGES_DIR, CUSTOM_LEVELS_DIR
from mode_create import Create


class CreateScreen(BaseScreen):
    def __init__(self, app, screen):
        super().__init__(app, screen, "menu.mp3")

        # TODO : Centrer les boutons
        buttons_x = WIDTH // 2 - 100
        self.main_buttons = [
            Button(screen=self.screen, x=buttons_x, y=100, width=200,
                   height=50, text="10X10", bg_color=GREEN, text_color=BLACK),
            Button(screen=self.screen, x=buttons_x, y=200, width=200,
                   height=50, text="15X15", bg_color=GREEN, text_color=BLACK),
            Button(screen=self.screen, x=buttons_x, y=300, width=200,
                   height=50, text="20X20", bg_color=GREEN, text_color=BLACK),
            Button(screen=self.screen, x=buttons_x, y=400, width=200,
                   height=50, text="Quit", bg_color=RED, text_color=BLACK),
        ]
        create_button_width = WIDTH // 7
        self.create_buttons = [
            Button(screen=self.screen, x=0, y=GRID_HEIGHT, width=create_button_width,
                   height=50, text="empty", bg_color=GREEN, text_color=BLACK),
            Button(screen=self.screen, x=create_button_width, y=GRID_HEIGHT, width=create_button_width,
                   height=50, text="wall", bg_color=GREEN, text_color=BLACK),
            Button(screen=self.screen, x=2*create_button_width, y=GRID_HEIGHT, width=create_button_width,
                   height=50, text="box", bg_color=GREEN, text_color=BLACK),
            Button(screen=self.screen, x=3*create_button_width, y=GRID_HEIGHT, width=create_button_width,
                   height=50, text="goal", bg_color=GREEN, text_color=BLACK),
            Button(screen=self.screen, x=4*create_button_width, y=GRID_HEIGHT, width=create_button_width,
                   height=50, text="player", bg_color=GREEN, text_color=BLACK),
            Button(screen=self.screen, x=5*create_button_width, y=GRID_HEIGHT, width=create_button_width,
                   height=50, text="save", bg_color=GREEN, text_color=BLACK),
            Button(screen=self.screen, x=6*create_button_width, y=GRID_HEIGHT, width=create_button_width,
                   height=50, text="quit", bg_color=GREEN, text_color=BLACK),
        ]
        self.current_screen = "main"
        self.creator = None
        self.cell_width = 0
        self.cell_height = 0
        self.images = []

    def update(self):
        if self.current_screen == "main":
            # TODO : Ajouter une image de fond
            for button in self.main_buttons:
                button.draw()
        elif self.current_screen == "create":
            self.draw_create()

    def draw_create(self):
        for y in range(self.creator.height):
            for x in range(self.creator.width):
                if self.creator.is_empty(x, y):
                    self.draw_cell(x, y, "empty_cell")
                elif self.creator.is_wall(x, y):
                    self.draw_cell(x, y, "wall")
                elif self.creator.is_box(x, y):
                    self.draw_cell(x, y, "box")
                elif self.creator.is_goal(x, y):
                    self.draw_cell(x, y, "goal")
                elif self.creator.is_player(x, y):
                    self.draw_cell(x, y, "player")

        for button in self.create_buttons:
            button.draw()

    def load_creator(self, width, height):
        self.current_screen = "create"
        self.creator = Create(width, height)
        self.cell_width = GRID_WIDTH // width
        self.cell_height = GRID_HEIGHT // height

        self.images = {
            "wall": self.load_img("wall.png"),
            "empty_cell": self.load_img("empty_cell.png"),
            "box": self.load_img("box.png"),
            "goal": self.load_img("goal.png"),
            "player": self.load_img("player_down.png"),
        }

    def load_img(self, filename):
        return pygame.transform.scale(pygame.image.load(IMAGES_DIR / filename), (self.cell_width, self.cell_height))

    def draw_cell(self, x, y, img_name):
        self.screen.blit(self.images[img_name],
                         (x * self.cell_width, y * self.cell_height))

    def handle_create_button(self, text):
        if text in ["empty", "wall", "box", "goal", "player"]:
            self.current_tool = text
        elif text == "save":
            self.creator.sauvegarder_niveau(CUSTOM_LEVELS_DIR / "level1.txt")
        elif text == "quit":
            self.app.switch_screen("menu")



    def handle_event(self, event):
        if self.current_screen == "main":
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.main_buttons:
                    if button.is_clicked(event.pos):
                        if button.text == "Quit":
                            self.app.switch_screen("menu")
                        else:
                            width, height = map(int, button.text.split("X"))
                            self.load_creator(width, height)
