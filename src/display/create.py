from pathlib import Path
import pygame

from .base import BaseScreen
from .widgets import ImageButton
from game.create_game import LevelCreator
from constants import BLUE, CELLS_IMAGES_DIR, FONT_PATH, HEIGHT, MAIN_MENU_BUTTON_PATH, MAIN_MENU_BUTTONS_HEIGHT, MAIN_MENU_BUTTONS_WIDTH, MAIN_MENU_BUTTONS_X, MAX_CUSTOM_LEVELS, MENU_BUTTON_HEIGHT, MENU_BUTTON_PATH, RED, WIDTH, BLACK, GRID_WIDTH, GRID_HEIGHT,  CUSTOM_LEVELS_DIR


class CreateScreen(BaseScreen):
    def __init__(self, app, screen):
        super().__init__(app=app, screen=screen, music="create.mp3", background_image_file="create.png")
        CUSTOM_LEVELS_DIR.mkdir(exist_ok=True, parents=True)
        # TODO : Centrer les boutons
        self.main_buttons = []
        for i, path in enumerate(CUSTOM_LEVELS_DIR.iterdir()):
            x = (WIDTH - 2*MAIN_MENU_BUTTONS_WIDTH) // 2
            level_button = ImageButton(screen=screen,
                                       x=x,
                                       y=i*2*MAIN_MENU_BUTTONS_HEIGHT + MAIN_MENU_BUTTONS_HEIGHT,
                                       width=MAIN_MENU_BUTTONS_WIDTH,
                                       height=MAIN_MENU_BUTTONS_HEIGHT,
                                       text=path.stem.title(),
                                       background_image_file=MAIN_MENU_BUTTON_PATH,
                                       data=path)
            delete_button = ImageButton(screen=screen,
                                        x=x + MAIN_MENU_BUTTONS_WIDTH,
                                        y=i*2*MAIN_MENU_BUTTONS_HEIGHT + MAIN_MENU_BUTTONS_HEIGHT,
                                        width=MAIN_MENU_BUTTONS_WIDTH,
                                        height=MAIN_MENU_BUTTONS_HEIGHT,
                                        text="Delete",
                                        background_image_file=MAIN_MENU_BUTTON_PATH,
                                        data="delete_" + str(path))
            self.main_buttons += [level_button, delete_button]
        if len(self.main_buttons) < MAX_CUSTOM_LEVELS:
            y_create_levels_start = self.main_buttons[-1].y + MAIN_MENU_BUTTONS_HEIGHT*2 if self.main_buttons else 2*MAIN_MENU_BUTTONS_HEIGHT
            self.main_buttons += [
                ImageButton(screen=screen, x=MAIN_MENU_BUTTONS_X, y=y_create_levels_start, width=MAIN_MENU_BUTTONS_WIDTH, height=MAIN_MENU_BUTTONS_HEIGHT, text="New 10 X 10", background_image_file=MAIN_MENU_BUTTON_PATH, data=(10, 10)),
                ImageButton(screen=screen, x=MAIN_MENU_BUTTONS_X, y=y_create_levels_start + MAIN_MENU_BUTTONS_HEIGHT*2, width=MAIN_MENU_BUTTONS_WIDTH, height=MAIN_MENU_BUTTONS_HEIGHT, text="New 15 X 15", background_image_file=MAIN_MENU_BUTTON_PATH, data=(15, 15)),
                ImageButton(screen=screen, x=MAIN_MENU_BUTTONS_X, y=y_create_levels_start + MAIN_MENU_BUTTONS_HEIGHT*4, width=MAIN_MENU_BUTTONS_WIDTH, height=MAIN_MENU_BUTTONS_HEIGHT, text="New 20 X 20", background_image_file=MAIN_MENU_BUTTON_PATH, data=(20, 20)),
                ]
        y_quit_button = self.main_buttons[-1].y + MAIN_MENU_BUTTONS_HEIGHT*2
        self.main_buttons.append(ImageButton(screen=screen, x=MAIN_MENU_BUTTONS_X, y=y_quit_button, width=MAIN_MENU_BUTTONS_WIDTH, height=MAIN_MENU_BUTTONS_HEIGHT, text="Main Menu", background_image_file=MAIN_MENU_BUTTON_PATH, data="quit"))
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
        self.is_new_level = False

        self.level_name = ""
        self.save_message = ""
        self.save_message_color = BLACK
        self.save_buttons = [
            ImageButton(screen=screen, x=MAIN_MENU_BUTTONS_X, y=HEIGHT // 2 + 100, width=MAIN_MENU_BUTTONS_WIDTH, height=MAIN_MENU_BUTTONS_HEIGHT, text="Save", background_image_file=MAIN_MENU_BUTTON_PATH, data="save"),
            ImageButton(screen=screen, x=MAIN_MENU_BUTTONS_X, y=HEIGHT // 2 + 200, width=MAIN_MENU_BUTTONS_WIDTH, height=MAIN_MENU_BUTTONS_HEIGHT, text="Cancel", background_image_file=MAIN_MENU_BUTTON_PATH, data="cancel"),
        ]

    def update(self):
        if self.current_screen == "main":
            self.draw_main()
        elif self.current_screen == "create":
            self.draw_create()
        elif self.current_screen == "save":
            self.draw_save()

    def draw_save(self):
        font = pygame.font.Font(FONT_PATH, 30)

        self.draw_text(text="Enter your name : ", color=BLACK, font=font, center=(WIDTH // 2, HEIGHT // 2 - 100))
        self.draw_text(text=self.level_name, color=BLACK, font=font, center=(WIDTH // 2, HEIGHT // 2))
        self.draw_text(text=self.save_message, color=self.save_message_color, font=font, center=(WIDTH // 2, HEIGHT // 2 - 200))

        for button in self.save_buttons:
            self.draw_button(button)

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
            self.draw_button(button)
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

                self.draw_text(text=str(count), color=BLACK, font=font, center=(x, y))
                
        text_surface = font.render(self.create_message, True, self.create_message_color)
        x = 6 * self.create_button_width
        y = GRID_HEIGHT + MENU_BUTTON_HEIGHT + text_surface.get_height()
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    def load_creator(self, creator):
        self.current_screen = "create"
        self.creator = creator
        self.cell_width = GRID_WIDTH // self.creator.width
        self.cell_height = GRID_HEIGHT // self.creator.height
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

    def load_save(self):
        if self.is_new_level:
            if not self.creator.is_complete():
                self.create_message = "Invalid level"
                self.create_message_color = RED
            elif len(list(CUSTOM_LEVELS_DIR.iterdir())) >= MAX_CUSTOM_LEVELS:
                self.create_message = "Too many levels"
                self.create_message_color = RED
            else:
                self.current_screen = "save"
        else:
            self.save_level()

    def draw_cell(self, x, y, img_name):
        self.screen.blit(self.images[img_name],
                         (x * self.cell_width, y * self.cell_height))

    def is_tool_button(self, button):
        return button.data in ["empty", "wall", "box", "goal", "player"]
    
    def handle_create_button(self, button):
        if self.is_tool_button(button):
            self.change_tool(button.data)
        elif button.data == "save":
            self.load_save()
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
                        elif type(button.data) == str:
                            if button.data.startswith("delete_"):
                                path = Path(button.data.replace("delete_", ""))
                                path.unlink()
                                self.main_buttons.remove(button)
                                self.main_buttons = [button for button in self.main_buttons if  button.data != path]
                        elif type(button.data) == tuple:
                            creator = LevelCreator(*button.data)
                            self.load_creator(creator)
                            self.is_new_level = True
                        else:
                            creator = LevelCreator.from_file(button.data)
                            self.level_name = button.data.stem
                            self.load_creator(creator)

        elif self.current_screen == "create":
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.create_buttons:
                    if button.is_clicked(event.pos):
                        if self.create_message == "Invalid level":
                            self.create_message = ""
                            self.create_message_color = BLACK
                        self.handle_create_button(button)
                self.handle_grid_click(event.pos)

        elif self.current_screen == "save":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.save_level()
                elif event.key == pygame.K_BACKSPACE:
                    self.level_name = self.level_name [:-1]
                else:
                    self.level_name += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.save_buttons:
                    if button.is_clicked(event.pos):
                        if button.data == "save":
                            self.save_level()
                        elif button.data == "cancel":
                            self.current_screen = "create"

    def save_level(self):
        # TODO : vérifier si il n'existe pas déja
        CUSTOM_LEVELS_DIR.mkdir(exist_ok=True, parents=True)
        path = CUSTOM_LEVELS_DIR / f"{self.level_name}.txt"
        if path.exists() and self.is_new_level:
            self.save_message = "Level already exists"
            self.save_message_color = RED
            return
        self.creator.save(CUSTOM_LEVELS_DIR / f"{self.level_name}.txt")
        self.app.switch_screen("menu")
    