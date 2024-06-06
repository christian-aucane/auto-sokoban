import pygame


class BaseButton:
    def __init__(self,
                 screen,
                 x,
                 y,
                 width,
                 height,
                 text,
                 text_color,
                 font,
                 data=None):
        self.screen = screen
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.data = data
        self.font = font
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
                 background_image_path,
                 text_color,
                 font,
                 data=None):
        super().__init__(
            screen=screen,
            x=x,
            y=y,
            width=width,
            height=height,
            text=text,
            text_color=text_color,
            font=font,
            data=data
        )
        self.background_image = pygame.transform.scale(
            pygame.image.load(background_image_path),
            (self.width, self.height)
        )

    def draw_background_image(self):
        self.screen.blit(self.background_image, self.rect)
    
    def draw(self):
        self.draw_background_image()
        self.draw_text()


class Slider: 
    def __init__(self, screen, x, y, width, height, min_value, max_value, initial_value, bg_color, slider_color, knob_color, font, text_color,label=None, data=None):
        self.screen = screen
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.label = label
        self.data = data
        self.font = font
        self.text_color = text_color

        self.min_value = min_value
        self.max_value = max_value
        self._value = initial_value

        self.knob_pos = (self.value - self.min_value) / (self.max_value - self.min_value) * (width - 20)

        self.dragging = False

        # Couleurs
        self.bg_color = bg_color
        self.slider_color = slider_color
        self.knob_color = knob_color

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, new_value):
        self._value = min(max(new_value, self.min_value), self.max_value)
        self.knob_pos = (self.value - self.min_value) / (self.max_value - self.min_value) * (self.rect.width - 20)

    def draw(self):
        self.image.fill(self.bg_color)

        if self.label is not None:
            label_text_surface = self.font.render(self.label, True, self.text_color)
            label_text_rect = label_text_surface.get_rect(bottomleft=self.rect.topleft)
            self.screen.blit(label_text_surface, label_text_rect)

        pygame.draw.rect(self.image, self.slider_color, (10, self.rect.height // 2 - 5, self.rect.width - 20, 10))

        pygame.draw.rect(self.image, self.knob_color, (self.knob_pos, self.rect.height // 2 - 10, 20, 20))

        self.screen.blit(self.image, self.rect.topleft)

        text_surface = self.font.render(str(self.value), True, self.text_color)
        text_rect = text_surface.get_rect(topleft=self.rect.topright)
        self.screen.blit(text_surface, text_rect)

    def move_knob(self, pos):
        new_knob_pos = pos[0] - self.rect.x - 10
        self.knob_pos = min(max(new_knob_pos, 0), self.rect.width - 20)
        self.value = int(self.min_value + (self.max_value - self.min_value) * self.knob_pos / (self.rect.width - 20))

    def is_clicked(self, pos):
        if self.rect.collidepoint(pos):
            self.dragging = True
            return True
        return False

    def stop_dragging(self):
        self.dragging = False
