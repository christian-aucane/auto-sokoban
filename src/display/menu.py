import pygame

from .base import BaseScreen
from utils.widgets import ImageButton
from constants import Sizes, Paths, MAIN_MENU_BUTTONS_X


class MenuScreen(BaseScreen):
    def __init__(self, app, screen):
        super().__init__(
            "menu",
            app=app,
            screen=screen,
            background_image_path= Paths.BACKGROUND_IMAGES / "menu.png",
        )
        self.main_buttons = [
            ImageButton(
                screen=screen,
                x=MAIN_MENU_BUTTONS_X,
                y=100,
                width=Sizes.MAIN_MENU_BUTTON_WIDTH,
                height=Sizes.MAIN_MENU_BUTTON_HEIGHT,
                text="Play",
                background_image_file=Paths.MAIN_MENU_BUTTON,
                data="play"
            ),
            ImageButton(
                screen=screen,
                x=MAIN_MENU_BUTTONS_X,
                y=200,
                width=Sizes.MAIN_MENU_BUTTON_WIDTH,
                height=Sizes.MAIN_MENU_BUTTON_HEIGHT,
                text="Settings",
                background_image_file=Paths.MAIN_MENU_BUTTON,
                data="settings"
            ),
            ImageButton(
                screen=screen,
                x=MAIN_MENU_BUTTONS_X,
                y=300,
                width=Sizes.MAIN_MENU_BUTTON_WIDTH,
                height=Sizes.MAIN_MENU_BUTTON_HEIGHT,
                text="Create",
                background_image_file=Paths.MAIN_MENU_BUTTON,
                data="create"
            ),
            ImageButton(
                screen=screen,
                x=MAIN_MENU_BUTTONS_X,
                y=400,
                width=Sizes.MAIN_MENU_BUTTON_WIDTH,
                height=Sizes.MAIN_MENU_BUTTON_HEIGHT,
                text="Quit",
                background_image_file=Paths.MAIN_MENU_BUTTON,
                data="quit"
            )
        ]
        self.current_screen = "main"

        self.sound_manager.load_sound_effect("click", Paths.SOUND_EFFECTS / "click.mp3")
    
    def update(self):
        if self.current_screen == "main":
            self.draw_main()
        
    def handle_event(self, event):
        if self.current_screen == "main":
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.main_buttons:
                    if button.is_clicked(event.pos):
                        self.sound_manager.play_sound_effect("click")
                        if button.data == "play":
                            self.app.switch_screen("game")
                        elif button.data == "settings":
                            self.app.switch_screen("settings")
                        elif button.data == "create":
                            self.app.switch_screen("create")
                        elif button.data == "quit":
                            pygame.time.delay(800)
                            self.app.quit()
