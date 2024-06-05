from pathlib import Path
import pygame

from .base import BaseScreen
from .widgets import ImageButton
from game.create_game import LevelCreator
from constants import FONT, Sizes, Colors, Paths, MAIN_MENU_BUTTONS_X, MAX_CUSTOM_LEVELS


class CreateScreen(BaseScreen):
    def __init__(self, app, screen):
        super().__init__(app=app, screen=screen, music_name="create", background_image_file="create.png")
        Paths.CUSTOM_LEVELS.mkdir(exist_ok=True, parents=True)
        self.main_buttons = []
        for i, path in enumerate(Paths.CUSTOM_LEVELS.iterdir()):
            x = (Sizes.WIDTH - Sizes.MAIN_MENU_BUTTONS_WIDTH - Sizes.MAIN_MENU_BUTTONS_HEIGHT) // 2
            y = i*2*Sizes.MAIN_MENU_BUTTONS_HEIGHT + Sizes.MAIN_MENU_BUTTONS_HEIGHT
            level_button = ImageButton(screen=screen,
                                       x=x,
                                       y=y,
                                       width=Sizes.MAIN_MENU_BUTTONS_WIDTH,
                                       height=Sizes.MAIN_MENU_BUTTONS_HEIGHT,
                                       text=path.stem.title(),
                                       background_image_file=Paths.MAIN_MENU_BUTTON,
                                       data=path)
            delete_button = ImageButton(screen=screen,
                                        x=x + Sizes.MAIN_MENU_BUTTONS_WIDTH,
                                        y=y,
                                        width=Sizes.MAIN_MENU_BUTTONS_HEIGHT,
                                        height=Sizes.MAIN_MENU_BUTTONS_HEIGHT,
                                        text="",
                                        background_image_file=Paths.DELETE_BUTTON,
                                        data="delete_" + str(path))
            self.main_buttons += [level_button, delete_button]
        if len(self.main_buttons) < 2*MAX_CUSTOM_LEVELS:
            if self.main_buttons:
                y_create_levels_start = self.main_buttons[-1].y + Sizes.MAIN_MENU_BUTTONS_HEIGHT*2
            else:
                y_create_levels_start = 2*Sizes.MAIN_MENU_BUTTONS_HEIGHT
            self.main_buttons += [
                ImageButton(
                    screen=screen,
                    x=MAIN_MENU_BUTTONS_X,
                    y=y_create_levels_start,
                    width=Sizes.MAIN_MENU_BUTTONS_WIDTH,
                    height=Sizes.MAIN_MENU_BUTTONS_HEIGHT,
                    text="New 10 X 10",
                    background_image_file=Paths.MAIN_MENU_BUTTON,
                    data=(10, 10)
                ),
                ImageButton(
                    screen=screen,
                    x=MAIN_MENU_BUTTONS_X,
                    y=y_create_levels_start + Sizes.MAIN_MENU_BUTTONS_HEIGHT*2,
                    width=Sizes.MAIN_MENU_BUTTONS_WIDTH,
                    height=Sizes.MAIN_MENU_BUTTONS_HEIGHT,
                    text="New 15 X 15",
                    background_image_file=Paths.MAIN_MENU_BUTTON,
                    data=(15, 15)
                ),
                ImageButton(
                    screen=screen,
                    x=MAIN_MENU_BUTTONS_X,
                    y=y_create_levels_start + Sizes.MAIN_MENU_BUTTONS_HEIGHT*4,
                    width=Sizes.MAIN_MENU_BUTTONS_WIDTH,
                    height=Sizes.MAIN_MENU_BUTTONS_HEIGHT,
                    text="New 20 X 20",
                    background_image_file=Paths.MAIN_MENU_BUTTON,
                    data=(20, 20)
                ),
            ]
        y_quit_button = self.main_buttons[-1].y + Sizes.MAIN_MENU_BUTTONS_HEIGHT*2
        self.main_buttons.append(ImageButton(screen=screen, x=MAIN_MENU_BUTTONS_X, y=y_quit_button, width=Sizes.MAIN_MENU_BUTTONS_WIDTH, height=Sizes.MAIN_MENU_BUTTONS_HEIGHT, text="Main Menu", background_image_file=Paths.MAIN_MENU_BUTTON, data="quit"))
        self.create_button_width = Sizes.WIDTH // 7
        self.create_buttons = [
            ImageButton(
                screen=screen,
                x=0,
                y=Sizes.GRID_HEIGHT,
                width=self.create_button_width,
                height=Sizes.MENU_BUTTON_HEIGHT,
                text="Empty",
                background_image_file=Paths.MENU_BUTTON,
                data="empty"
            ),
            ImageButton(
                screen=screen,
                x=self.create_button_width,
                y=Sizes.GRID_HEIGHT,
                width=self.create_button_width,
                height=Sizes.MENU_BUTTON_HEIGHT,
                text="Wall",
                background_image_file=Paths.MENU_BUTTON,
                data="wall"
            ),
            ImageButton(
                screen=screen,
                x=2 * self.create_button_width,
                y=Sizes.GRID_HEIGHT,
                width=self.create_button_width,
                height=Sizes.MENU_BUTTON_HEIGHT,
                text="Box",
                background_image_file=Paths.MENU_BUTTON,
                data="box"
            ),
            ImageButton(
                screen=screen,
                x=3 * self.create_button_width,
                y=Sizes.GRID_HEIGHT,
                width=self.create_button_width,
                height=Sizes.MENU_BUTTON_HEIGHT,
                text="Goal",
                background_image_file=Paths.MENU_BUTTON,
                data="goal"
            ),
            ImageButton(
                screen=screen,
                x=4 * self.create_button_width,
                y=Sizes.GRID_HEIGHT,
                width=self.create_button_width,
                height=Sizes.MENU_BUTTON_HEIGHT,
                text="Player",
                background_image_file=Paths.MENU_BUTTON,
                data="player"
            ),
            ImageButton(
                screen=screen,
                x=5 * self.create_button_width,
                y=Sizes.GRID_HEIGHT,
                width=self.create_button_width,
                height=Sizes.MENU_BUTTON_HEIGHT,
                text="Save",
                background_image_file=Paths.MENU_BUTTON,
                data="save"
            ),
            ImageButton(
                screen=screen,
                x=6 * self.create_button_width,
                y=Sizes.GRID_HEIGHT,
                width=self.create_button_width,
                height=Sizes.MENU_BUTTON_HEIGHT,
                text="Menu",
                background_image_file=Paths.MENU_BUTTON,
                data="quit"
            ),
        ]
        self.current_screen = "main"
        self.creator = None
        self.cell_width = 0
        self.cell_height = 0
        self.images = []
        self.create_message = ""
        self.create_message_color = Colors.BLACK
        self.is_new_level = False

        self.level_name = ""
        self.save_message = ""
        self.save_message_color = Colors.BLACK
        self.save_buttons = [
            ImageButton(
                screen=screen,
                x=MAIN_MENU_BUTTONS_X,
                y=Sizes.HEIGHT // 2 + 100,
                width=Sizes.MAIN_MENU_BUTTONS_WIDTH,
                height=Sizes.MAIN_MENU_BUTTONS_HEIGHT,
                text="Save",
                background_image_file=Paths.MAIN_MENU_BUTTON,
                data="save"
            ),
            ImageButton(
                screen=screen,
                x=MAIN_MENU_BUTTONS_X,
                y=Sizes.HEIGHT // 2 + 200,
                width=Sizes.MAIN_MENU_BUTTONS_WIDTH,
                height=Sizes.MAIN_MENU_BUTTONS_HEIGHT,
                text="Cancel",
                background_image_file=Paths.MAIN_MENU_BUTTON,
                data="cancel"
            ),
        ]

    def update(self):
        if self.current_screen == "main":
            self.draw_main()
        elif self.current_screen == "create":
            self.draw_create()
        elif self.current_screen == "save":
            self.draw_save()

    def draw_save(self):
        self.draw_text(
            text="Enter grid name : ",
            color=Colors.BLACK,
            center=(Sizes.WIDTH // 2, Sizes.HEIGHT // 2 - 100)
        )
        self.draw_text(
            text=self.level_name,
            color=Colors.BLACK,
            center=(Sizes.WIDTH // 2, Sizes.HEIGHT // 2)
        )
        self.draw_text(
            text=self.save_message,
            color=self.save_message_color,
            center=(Sizes.WIDTH // 2, Sizes.HEIGHT // 2 - 200)
        )

        for button in self.save_buttons:
            self.draw_button(button)

    def change_tool(self, tool):
        self.creator.current_tool = tool

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

        for button in self.create_buttons:
            is_active = self.creator.current_tool == button.data
            self.draw_button(button, is_active=is_active)
            counter = self.creator.counter
            if self.is_tool_button(button):
                x = button.x
                y = button.y + button.height
                
                img = pygame.transform.scale(
                    self.images[button.data],
                    (button.height, button.height)
                )
                self.screen.blit(img,(x , y))
                count = counter[button.data]

                x = x + button.height + 10
                y = y + button.height // 2

                self.draw_text(text=str(count), color=Colors.BLACK, center=(x, y))
                
        text_surface = FONT.render(self.create_message, True, self.create_message_color)
        x = 6 * self.create_button_width
        y = Sizes.GRID_HEIGHT + Sizes.MENU_BUTTON_HEIGHT + text_surface.get_height()
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    def load_creator(self, creator):
        self.current_screen = "create"
        self.creator = creator
        self.cell_width = Sizes.GRID_WIDTH // self.creator.width
        self.cell_height = Sizes.GRID_HEIGHT // self.creator.height
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
        return pygame.transform.scale(
            pygame.image.load(Paths.CELLS_IMAGES / filename),
            (width, height)
        )

    def load_save(self):
        if self.is_new_level:
            if not self.creator.is_complete():
                self.create_message = "Invalid level"
                self.create_message_color = Colors.ERROR
            elif len(list(Paths.CUSTOM_LEVELS.iterdir())) >= MAX_CUSTOM_LEVELS:
                self.create_message = "Too many levels"
                self.create_message_color = Colors.ERROR
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
        if y >= Sizes.GRID_HEIGHT:
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
                                self.main_buttons = [
                                    button for button in self.main_buttons
                                    if button.data != path
                                ]
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
                            self.create_message_color = Colors.BLACK
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
        Paths.CUSTOM_LEVELS.mkdir(exist_ok=True, parents=True)
        path = Paths.CUSTOM_LEVELS / f"{self.level_name}.txt"
        if path.exists() and self.is_new_level:
            self.save_message = "Level already exists"
            self.save_message_color = Colors.ERROR
            return
        self.creator.save(Paths.CUSTOM_LEVELS / f"{self.level_name}.txt")
        self.app.switch_screen("menu")
    