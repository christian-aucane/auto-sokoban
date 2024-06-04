import pygame

from .base import BaseScreen
from .widgets import ImageButton
from constants import MAIN_MENU_BUTTON_PATH, MAIN_MENU_BUTTONS_HEIGHT, MAIN_MENU_BUTTONS_WIDTH, MAIN_MENU_BUTTONS_X


class MenuScreen(BaseScreen):
    def __init__(self, app, screen):
        super().__init__(app=app, screen=screen, music="menu.mp3", background_image_file="menu.png")

        self.main_buttons = [
            ImageButton(screen=screen, x=MAIN_MENU_BUTTONS_X, y=100, width=MAIN_MENU_BUTTONS_WIDTH, height=MAIN_MENU_BUTTONS_HEIGHT, text="Play", background_image_file=MAIN_MENU_BUTTON_PATH, data="play"),
            ImageButton(screen=screen, x=MAIN_MENU_BUTTONS_X, y=200, width=MAIN_MENU_BUTTONS_WIDTH, height=MAIN_MENU_BUTTONS_HEIGHT, text="Settings", background_image_file=MAIN_MENU_BUTTON_PATH, data="settings"),
            ImageButton(screen=screen, x=MAIN_MENU_BUTTONS_X, y=300, width=MAIN_MENU_BUTTONS_WIDTH, height=MAIN_MENU_BUTTONS_HEIGHT, text="Create", background_image_file=MAIN_MENU_BUTTON_PATH, data="create"),
            ImageButton(screen=screen, x=MAIN_MENU_BUTTONS_X, y=400, width=MAIN_MENU_BUTTONS_WIDTH, height=MAIN_MENU_BUTTONS_HEIGHT, text="Player", background_image_file=MAIN_MENU_BUTTON_PATH, data="player"),  # Nouveau bouton
            ImageButton(screen=screen, x=MAIN_MENU_BUTTONS_X, y=500, width=MAIN_MENU_BUTTONS_WIDTH, height=MAIN_MENU_BUTTONS_HEIGHT, text="Quit", background_image_file=MAIN_MENU_BUTTON_PATH, data="quit"),
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
                        if button.data == "play":
                            self.app.switch_screen("game")
                        elif button.data == "settings":
                            # TODO : faire un menu settings
                            print("SETTINGS")
                        elif button.data == "create":
                            self.app.switch_screen("create")
                        elif button.data == "player":  # Gérer le clic sur le nouveau bouton
                            self.app.switch_screen("player")
                        elif button.data == "quit":
                            self.app.quit()
