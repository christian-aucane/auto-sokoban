import pygame
from .base import BaseScreen
from .widgets import ImageButton
from constants import MAIN_MENU_BUTTONS_HEIGHT, MAIN_MENU_BUTTONS_WIDTH, MAIN_MENU_BUTTONS_X, MAIN_MENU_BUTTON_PATH


class SimpleTextBox:
    def __init__(self, x, y, width, height, text_color=(0, 0, 0), background_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text_color = text_color
        self.background_color = background_color
        self.text = ''
        self.font = pygame.font.Font(None, 32)
  
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print(self.text)
                self.text = ''
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

    def draw(self, screen):
        pygame.draw.rect(screen, self.background_color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        screen.blit(text_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.text_color, self.rect, 2)

    def get_text(self):
        return self.text


class PlayerScreen(BaseScreen):
    def __init__(self, app, screen):
        super().__init__(app=app, screen=screen, music="menu.mp3", background_image_file="menu.png")
        self.font = pygame.font.Font(None, 32)
        self.player_buttons = [
            ImageButton(screen=screen, x=MAIN_MENU_BUTTONS_X, y=100, width=MAIN_MENU_BUTTONS_WIDTH, height=MAIN_MENU_BUTTONS_HEIGHT, text="Create Player", background_image_file=MAIN_MENU_BUTTON_PATH, data="create_player"),
        ]

        self.player_name_box = SimpleTextBox(MAIN_MENU_BUTTONS_X + MAIN_MENU_BUTTONS_WIDTH + 10, 100, MAIN_MENU_BUTTONS_WIDTH, MAIN_MENU_BUTTONS_HEIGHT)
        self.selected_player = None

        # Create a new surface for the player list
        self.player_list_surface = pygame.Surface((300, 500))  # Adjust the size as needed
        self.player_list_surface.fill((255, 255, 255))  # Fill with white color

    def update(self):
        self.draw_main()
        self.player_name_box.draw(self.screen)
        for button in self.player_buttons:
            button.draw()

        # Draw the player list on the new surface
        players = self.app.player_manager.get_all_players()
        for i, player in enumerate(players):
            player_text = self.font.render(player, True, (0, 0, 0))
            self.player_list_surface.blit(player_text, (10, i * 40))  # Adjust the position as needed

        # Draw the new surface on the screen
        self.screen.blit(self.player_list_surface, (MAIN_MENU_BUTTONS_X, 200))  # Adjust the position as needed

    def handle_event(self, event):
        self.player_name_box.handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.player_buttons:
                if button.is_clicked(event.pos):
                    player_name = self.player_name_box.get_text()
                    if button.data == "create_player":
                        self.app.player_manager.create_player(player_name)
                        self.player_name_box.text = ''
