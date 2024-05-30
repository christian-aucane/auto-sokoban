import pygame

from screens.base import BaseScreen
from widgets import Button
from constants import BLUE, MENU_HEIGHT, WIDTH, GREEN, RED, BLACK, GRID_WIDTH, GRID_HEIGHT, IMAGES_DIR, CUSTOM_LEVELS_DIR, YELLOW
from create_game import LevelCreator


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
        self.create_button_width = WIDTH // 7
        self.create_button_height = MENU_HEIGHT // 2
        self.create_buttons = [
            Button(screen=self.screen, x=0, y=GRID_HEIGHT, width=self.create_button_width,
                   height=self.create_button_height, text="empty", bg_color=BLUE, text_color=BLACK),
            Button(screen=self.screen, x=self.create_button_width, y=GRID_HEIGHT, width=self.create_button_width,
                   height=self.create_button_height, text="wall", bg_color=BLUE, text_color=BLACK),
            Button(screen=self.screen, x=2*self.create_button_width, y=GRID_HEIGHT, width=self.create_button_width,
                   height=self.create_button_height, text="box", bg_color=BLUE, text_color=BLACK),
            Button(screen=self.screen, x=3*self.create_button_width, y=GRID_HEIGHT, width=self.create_button_width,
                   height=self.create_button_height, text="goal", bg_color=BLUE, text_color=BLACK),
            Button(screen=self.screen, x=4*self.create_button_width, y=GRID_HEIGHT, width=self.create_button_width,
                   height=self.create_button_height, text="player", bg_color=BLUE, text_color=BLACK),
            Button(screen=self.screen, x=5*self.create_button_width, y=GRID_HEIGHT, width=self.create_button_width,
                   height=self.create_button_height, text="save", bg_color=GREEN, text_color=BLACK),
            Button(screen=self.screen, x=6*self.create_button_width, y=GRID_HEIGHT, width=self.create_button_width,
                   height=self.create_button_height, text="quit", bg_color=RED, text_color=BLACK),
        ]
        self.current_screen = "main"
        self.creator = None
        self.cell_width = 0
        self.cell_height = 0
        self.images = []
        self.create_message = ""
        self.create_message_color = BLACK

    def update(self):
        if self.current_screen == "main":
            # TODO : Ajouter une image de fond
            for button in self.main_buttons:
                button.draw()
        elif self.current_screen == "create":
            self.draw_create()

    def change_tool(self, tool):
        self.creator.current_tool = tool
        for button in self.create_buttons:
            if self.is_tool_button(button):
                if button.text == tool:
                    button.bg_color = YELLOW
                else:
                    button.bg_color = BLUE
                    button.text_color = BLACK

    def draw_create(self):
        for y in range(self.creator.height):
            for x in range(self.creator.width):
                if self.creator.is_empty(x, y):
                    self.draw_cell(x, y, "empty")
                elif self.creator.is_wall(x, y):
                    self.draw_cell(x, y, "wall")
                elif self.creator.is_box(x, y):
                    self.draw_cell(x, y, "box")
                elif self.creator.is_goal(x, y):
                    self.draw_cell(x, y, "goal")
                elif self.creator.is_player(x, y):
                    self.draw_cell(x, y, "player")


        font = pygame.font.SysFont("", 30)
        for button in self.create_buttons:
            button.draw()
            counter = self.creator.counter
            if self.is_tool_button(button):
                # TODO afficher une image et le compte en dessous
                x = button.x
                y = button.y + button.height
                
                img = pygame.transform.scale(self.images[button.text], (button.height, button.height))
                self.screen.blit(img,(x , y))
                count = counter[button.text]

                x = x + button.height + 10
                y = y + button.height // 2

                text_surface = font.render(str(count), True, BLACK)
                text_rect = text_surface.get_rect(center=(x, y))
                self.screen.blit(text_surface, text_rect)

        text_surface = font.render(self.create_message, True, self.create_message_color)
        x = 6 * self.create_button_width
        y = GRID_HEIGHT + self.create_button_height + text_surface.get_height()
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    def load_creator(self, width, height):
        self.current_screen = "create"
        self.creator = LevelCreator(width, height)
        self.cell_width = GRID_WIDTH // width
        self.cell_height = GRID_HEIGHT // height
        self.change_tool("empty")

        self.images = {
            "wall": self.load_img("wall.png"),
            "empty": self.load_img("empty_cell.png"),
            "box": self.load_img("box.png"),
            "goal": self.load_img("goal.png"),
            "player": self.load_img("player_down.png"),
        }

    def load_img(self, filename, width=None, height=None):
        if width is None:
            width = self.cell_width
        if height is None:
            height = self.cell_height
        return pygame.transform.scale(pygame.image.load(IMAGES_DIR / filename), (width, height))

    def draw_cell(self, x, y, img_name):
        self.screen.blit(self.images[img_name],
                         (x * self.cell_width, y * self.cell_height))

    def is_tool_button(self, button):
        return button.text in ["empty", "wall", "box", "goal", "player"]
    
    def handle_create_button(self, button):
        if self.is_tool_button(button):
            self.change_tool(button.text)
        elif button.text == "save":
            # TODO : créer un ecran pour choisir le nom ?
            CUSTOM_LEVELS_DIR.mkdir(parents=True, exist_ok=True)
            self.creator.save(CUSTOM_LEVELS_DIR / "level1.txt")
        elif button.text == "quit":
            self.app.switch_screen("menu")

    def handle_grid_click(self, pos):
        x, y = pos
        if y >= GRID_HEIGHT:
            return
        self.creator.put(x // self.cell_width, y // self.cell_height)

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

        elif self.current_screen == "create":
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.create_buttons:
                    if button.is_clicked(event.pos):
                        self.handle_create_button(button)
                self.handle_grid_click(event.pos)
