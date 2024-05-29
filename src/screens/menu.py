import pygame

from screens.base import BaseScreen
from widgets import Button
from constants import WIDTH, GREEN, YELLOW, BLUE, RED, BLACK



class MenuScreen(BaseScreen):
    def __init__(self, app, screen):
        super().__init__(app, screen, "menu.mp3")

        # TODO : Centrer les boutons
        buttons_x = WIDTH // 2 - 100
        self.main_buttons = [
            Button(screen=self.screen, x=buttons_x, y=100, width=200, height=50, text="Play", bg_color=GREEN, text_color=BLACK),
            Button(screen=self.screen, x=buttons_x, y=200, width=200, height=50, text="Settings", bg_color=YELLOW, text_color=BLACK),
            Button(screen=self.screen, x=buttons_x, y=300, width=200, height=50, text="Create", bg_color=BLUE, text_color=BLACK),
            Button(screen=self.screen, x=buttons_x, y=400, width=200, height=50, text="Quit", bg_color=RED, text_color=BLACK),
        ]
        self.current_screen = "main"
    
    def update(self):
        if self.current_screen == "main":
        # TODO : Ajouter une image de fond
            for button in self.main_buttons:
                button.draw()
        
    def handle_event(self, event):
        if self.current_screen == "main":
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.main_buttons:
                    if button.is_clicked(event.pos):
                        if button.text == "Play":
                            self.app.switch_screen("game")
                        elif button.text == "Settings":
                            # TODO : faire un menu settings
                            print("SETTINGS")
                        elif button.text == "Create":
                            self.app.switch_screen("create")
                        elif button.text == "Quit":
                            self.app.quit()
