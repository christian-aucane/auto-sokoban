import pygame

from .base import BaseScreen
from .widgets import ImageButton
from game.create_game import LevelCreator
from constants import BLUE, CELLS_IMAGES_DIR, FONT_PATH, MAIN_MENU_BUTTON_PATH, MAIN_MENU_BUTTONS_HEIGHT, MAIN_MENU_BUTTONS_WIDTH, MAIN_MENU_BUTTONS_X, MENU_BUTTON_HEIGHT, MENU_BUTTON_PATH, WIDTH, BLACK, GRID_WIDTH, GRID_HEIGHT,  CUSTOM_LEVELS_DIR


class CreateScreen(BaseScreen):
    def __init__(self, app, screen):
        super().__init__(app=app, screen=screen, music="create.mp3", background_image_file="create.png")

        # TODO : Centrer les boutons
        self.main_buttons = [
            ImageButton(screen=screen, x=MAIN_MENU_BUTTONS_X, y=100, width=MAIN_MENU_BUTTONS_WIDTH, height=MAIN_MENU_BUTTONS_HEIGHT, text="10 X 10", background_image_file=MAIN_MENU_BUTTON_PATH, data=(10, 10)),
            ImageButton(screen=screen, x=MAIN_MENU_BUTTONS_X, y=200, width=MAIN_MENU_BUTTONS_WIDTH, height=MAIN_MENU_BUTTONS_HEIGHT, text="15 X 15", background_image_file=MAIN_MENU_BUTTON_PATH, data=(15, 15)),
            ImageButton(screen=screen, x=MAIN_MENU_BUTTONS_X, y=300, width=MAIN_MENU_BUTTONS_WIDTH, height=MAIN_MENU_BUTTONS_HEIGHT, text="20 X 20", background_image_file=MAIN_MENU_BUTTON_PATH, data=(20, 20)),
            ImageButton(screen=screen, x=MAIN_MENU_BUTTONS_X, y=400, width=MAIN_MENU_BUTTONS_WIDTH, height=MAIN_MENU_BUTTONS_HEIGHT, text="Main Menu", background_image_file=MAIN_MENU_BUTTON_PATH, data="quit"),
        ]
        self.create_button_width = WIDTH // 7
        self.create_buttons = [
            ImageButton(screen=screen, x=0, y=GRID_HEIGHT, width=self.create_button_width, height=MENU_BUTTON_HEIGHT, text="Empty", background_image_file=MENU_BUTTON_PATH, data="empty"),
            ImageButton(screen=screen, x=self.create_button_width, y=GRID_HEIGHT, width=self.create_button_width, height=MENU_BUTTON_HEIGHT, text="Wall", background_image_file=MENU_BUTTON_PATH, data="wall"),
            ImageButton(screen=screen, x=2 * self.create_button_width, y=GRID_HEIGHT, width=self.create_button_width, height=MENU_BUTTON_HEIGHT, text="Box", background_image_file=MENU_BUTTON_PATH, data="box"),
            ImageButton(screen=screen, x=3 * self.create_button_width, y=GRID_HEIGHT, width=self.create_button_width, height=MENU_BUTTON_HEIGHT, text="Goal", background_image_file=MENU_BUTTON_PATH, data="goal"),
            ImageButton(screen=screen, x=4 * self.create_button_width, y=GRID_HEIGHT, width=self.create_button_width, height=MENU_BUTTON_HEIGHT, text="Player", background_image_file=MENU_BUTTON_PATH, data="player"),
            ImageButton(screen=screen, x=5 * self.create_button_width, y=GRID_HEIGHT, width=self.create_button_width, height=MENU_BUTTON_HEIGHT, text="Save", background_image_file=MENU_BUTTON_PATH, data="save"),
            ImageButton(screen=screen, x=6 * self.create_button_width, y=GRID_HEIGHT, width=self.create_button_width, height=MENU_BUTTON_HEIGHT, text="Menu", background_image_file=MENU_BUTTON_PATH, data="quit"),
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
            self.draw_main()
        elif self.current_screen == "create":
            self.draw_create()

    def change_tool(self, tool):
        self.creator.current_tool = tool
        for button in self.create_buttons:
            if self.is_tool_button(button):
                if button.data == tool:
                    button.set_text_color(BLUE)
                else:
                    button.set_text_color(BLACK)

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


        font = pygame.font.Font(FONT_PATH, 30)
        for button in self.create_buttons:
            button.draw()
            counter = self.creator.counter
            if self.is_tool_button(button):
                # TODO afficher une image et le compte en dessous
                x = button.x
                y = button.y + button.height
                
                img = pygame.transform.scale(self.images[button.data], (button.height, button.height))
                self.screen.blit(img,(x , y))
                count = counter[button.data]

                x = x + button.height + 10
                y = y + button.height // 2

                text_surface = font.render(str(count), True, BLACK)
                text_rect = text_surface.get_rect(center=(x, y))
                self.screen.blit(text_surface, text_rect)

        text_surface = font.render(self.create_message, True, self.create_message_color)
        x = 6 * self.create_button_width
        y = GRID_HEIGHT + MENU_BUTTON_HEIGHT + text_surface.get_height()
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
        return pygame.transform.scale(pygame.image.load(CELLS_IMAGES_DIR / filename), (width, height))

    def draw_cell(self, x, y, img_name):
        self.screen.blit(self.images[img_name],
                         (x * self.cell_width, y * self.cell_height))

    def is_tool_button(self, button):
        return button.data in ["empty", "wall", "box", "goal", "player"]
    
    def handle_create_button(self, button):
        if self.is_tool_button(button):
            self.change_tool(button.data)
        elif button.data == "save":
            # TODO : créer un ecran pour choisir le nom ?
            CUSTOM_LEVELS_DIR.mkdir(parents=True, exist_ok=True)
            self.creator.save(CUSTOM_LEVELS_DIR / "level1.txt")
        elif button.data == "quit":
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
                        if button.data == "quit":
                            self.app.switch_screen("menu")
                        else:
                            width, height = button.data
                            self.load_creator(width, height)

        elif self.current_screen == "create":
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.create_buttons:
                    if button.is_clicked(event.pos):
                        self.handle_create_button(button)
                self.handle_grid_click(event.pos)
