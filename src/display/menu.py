import pygame

from .base import BaseScreen
from .widgets import ImageButton
from constants import Sizes, Paths, MAIN_MENU_BUTTONS_X


class MenuScreen(BaseScreen):
    def __init__(self, app, screen):
        super().__init__(
            app=app,
            screen=screen,
            music_name="menu",
            background_image_file="menu.png",
            sound_effects={"click": self.load_sound_effect("game/click.mp3")},
        )
        self.main_buttons = [
            ImageButton(
                screen=screen,
                x=MAIN_MENU_BUTTONS_X,
                y=100,
                width=Sizes.MAIN_MENU_BUTTONS_WIDTH,
                height=Sizes.MAIN_MENU_BUTTONS_HEIGHT,
                text="Play",
                background_image_file=Paths.MAIN_MENU_BUTTON,
                data="play"
            ),
            ImageButton(
                screen=screen,
                x=MAIN_MENU_BUTTONS_X,
                y=200,
                width=Sizes.MAIN_MENU_BUTTONS_WIDTH,
                height=Sizes.MAIN_MENU_BUTTONS_HEIGHT,
                text="Settings",
                background_image_file=Paths.MAIN_MENU_BUTTON,
                data="settings"
            ),
            ImageButton(
                screen=screen,
                x=MAIN_MENU_BUTTONS_X,
                y=300,
                width=Sizes.MAIN_MENU_BUTTONS_WIDTH,
                height=Sizes.MAIN_MENU_BUTTONS_HEIGHT,
                text="Create",
                background_image_file=Paths.MAIN_MENU_BUTTON,
                data="create"
            ),
            ImageButton(
                screen=screen,
                x=MAIN_MENU_BUTTONS_X,
                y=400,
                width=Sizes.MAIN_MENU_BUTTONS_WIDTH,
                height=Sizes.MAIN_MENU_BUTTONS_HEIGHT,
                text="Quit",
                background_image_file=Paths.MAIN_MENU_BUTTON,
                data="quit"
            )
        ]
        self.current_screen = "main"
    
    def update(self):
        if self.current_screen == "main":
            self.draw_main()
        
    def handle_event(self, event):
        if self.current_screen == "main":
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.main_buttons:
                    if button.is_clicked(event.pos):
                        self.play_sound_effect("click")
                        if button.data == "play":
                            self.app.switch_screen("game")
                        elif button.data == "settings":
                            # TODO : faire un menu settings
                            print("SETTINGS")
                        elif button.data == "create":
                            self.app.switch_screen("create")
                        elif button.data == "quit":
                            pygame.time.delay(800)
                            self.app.quit()
