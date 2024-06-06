import pygame

from constants import FONT, Colors, Paths


class BaseButton:
    def __init__(self,
                 screen,
                 x,
                 y,
                 width,
                 height,
                 text,
                 data=None,
                 text_color=Colors.BUTTON_TEXT,
                 font_path=Paths.FONT,
                 font_size=30):
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
        raise NotImplementedError(
            "draw() method must be implemented in subclass"
        )
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    
    def draw_text(self):
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.screen.blit(text_surface, text_rect)

    def set_text_color(self, color):
        self.text_color = color


class ImageButton(BaseButton):
    def __init__(self,
                 screen,
                 x,
                 y,
                 width,
                 height,
                 text,
                 background_image_file,
                 data=None,
                 text_color=Colors.BLACK,
                 font_path=Paths.FONT,
                 font_size=30):
        super().__init__(
            screen,
            x,
            y,
            width,
            height,
            text,
            data,
            text_color,
            font_path,
            font_size
        )
        self.background_image = pygame.transform.scale(
            pygame.image.load(Paths.BUTTONS_IMAGES /background_image_file),
            (self.width, self.height)
        )

    def draw_background_image(self):
        self.screen.blit(self.background_image, self.rect)
    
    def draw(self):
        self.draw_background_image()
        self.draw_text()


class Slider: 
    def __init__(self, screen, x, y, width, height, min_value, max_value, initial_value, bg_color, slider_color, knob_color, font=FONT, label=None, data=None):
        self.screen = screen
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.label = label
        self.data = data
        self.font = font

        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value

        self.knob_pos = (self.value - self.min_value) / (self.max_value - self.min_value) * (width - 20)

        # Couleurs
        self.bg_color = bg_color
        self.slider_color = slider_color
        self.knob_color = knob_color

    def update(self):
        pass

    def draw(self):
        self.image.fill(self.bg_color)

        if self.label is not None:
            label_text_surface = self.font.render(self.label, True, Colors.BLACK)
            label_text_rect = label_text_surface.get_rect(bottomleft=self.rect.topleft)
            self.screen.blit(label_text_surface, label_text_rect)

        pygame.draw.rect(self.image, self.slider_color, (10, self.rect.height // 2 - 5, self.rect.width - 20, 10))

        pygame.draw.rect(self.image, self.knob_color, (self.knob_pos, self.rect.height // 2 - 10, 20, 20))

        self.screen.blit(self.image, self.rect.topleft)

        text_surface = self.font.render(str(self.value), True, Colors.BLACK)
        text_rect = text_surface.get_rect(topleft=self.rect.topright)
        self.screen.blit(text_surface, text_rect)


    def move_knob(self, pos):
        # Calcule la nouvelle position du bouton en fonction de la différence entre la position du clic et la position actuelle du bouton
        new_knob_pos = pos[0] - self.rect.x - 10  # 10 pour prendre en compte le décalage du rectangle slider à gauche
        self.knob_pos = min(max(new_knob_pos, 0), self.rect.width - 20)
        self.value = int(self.min_value + (self.max_value - self.min_value) * self.knob_pos / (self.rect.width - 20))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
