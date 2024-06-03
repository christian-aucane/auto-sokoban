import pygame

from constants import BUTTON_TEXT_COLOR, BUTTONS_IMAGES_DIR, FONT_PATH, BLACK


class BaseButton:
    def __init__(self, screen, x, y, width, height, text, data=None, text_color=BUTTON_TEXT_COLOR, font_path=FONT_PATH, font_size=30):
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
    def __init__(self, screen, x, y, width, height, text, background_image_file, data=None, text_color=BLACK, font_path=FONT_PATH, font_size=30):
        super().__init__(screen, x, y, width, height, text, data, text_color, font_path, font_size)
        self.background_image = pygame.transform.scale(pygame.image.load(BUTTONS_IMAGES_DIR /background_image_file), (self.width, self.height))

    def draw_background_image(self):
        self.screen.blit(self.background_image, self.rect)
    
    def draw(self):
        self.draw_background_image()
        self.draw_text()
