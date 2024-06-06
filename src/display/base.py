import pygame

from constants import FONT, Sizes, Colors, Paths


class BaseScreen:
    def __init__(self,name, app, screen, background_image_file=""):
        self.app = app
        self.screen = screen
        self.sound_manager = app.sound_manager
        self.background_image = pygame.transform.scale(
            pygame.image.load(Paths.BACKGROUND_IMAGES / background_image_file),
            (Sizes.WIDTH, Sizes.HEIGHT)
        )
        self.main_buttons = []
        self.name = name
    
    def draw_background_image(self):
        self.screen.blit(self.background_image, (0, 0))

    def draw_main(self):
        self.draw_background_image()
        for button in self.main_buttons:
            self.draw_button(button)

    def draw_button(self, button, is_active=False):
        if is_active:
            button.set_text_color(Colors.BUTTON_ACTIVE_TEXT)
        elif button.is_clicked(pygame.mouse.get_pos()):
            button.set_text_color(Colors.BUTTON_HOVER_TEXT)
        else:
            button.set_text_color(Colors.BUTTON_TEXT)
        button.draw()

    def draw_text(self, text, color, **pos):
        text_surface = FONT.render(text, True, color)
        text_rect = text_surface.get_rect(**pos)
        self.screen.blit(text_surface, text_rect)

    def quit(self):
        pass

    def load(self):
        self.sound_manager.play_music(self.name)
        ...

    def update(self):
        raise NotImplementedError("Subclass must implement abstract method")
    
    def handle_event(self, event):
        raise NotImplementedError("Subclass must implement abstract method")
