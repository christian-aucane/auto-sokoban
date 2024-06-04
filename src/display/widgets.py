import pygame

from constants import Colors, Paths


class BaseButton:
    def __init__(self, screen, x, y, width, height, text, data=None, text_color=Colors.BUTTON_TEXT, font_path=Paths.FONT, font_size=30):
        self.screen = screen
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.data = data
        self.font = pygame.font.Font(font_path, font_size)
        self.text_color = text_color
        self.width = width
        self.height = height
        self.x = x
        self.y = y

    def draw(self):
        raise NotImplementedError("draw method must be implemented in subclass")
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    
    def draw_text(self):
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.screen.blit(text_surface, text_rect)

    def set_text_color(self, color):
        self.text_color = color


class ImageButton(BaseButton):
    def __init__(self, screen, x, y, width, height, text, background_image_file, data=None, text_color=Colors.BLACK, font_path=Paths.FONT, font_size=30):
        super().__init__(screen, x, y, width, height, text, data, text_color, font_path, font_size)
        self.background_image = pygame.transform.scale(pygame.image.load(Paths.BUTTONS_IMAGES /background_image_file), (self.width, self.height))

    def draw_background_image(self):
        self.screen.blit(self.background_image, self.rect)
    
    def draw(self):
        self.draw_background_image()
        self.draw_text()
