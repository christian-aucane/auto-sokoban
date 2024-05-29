import pygame


class Button:
    """
    Button class for creating interactive buttons on a Pygame screen.

    Args:
        screen (pygame.Surface): The screen to draw the button on.
        x (int): The x coordinate of the button.
        y (int): The y coordinate of the button.
        width (int): The width of the button.
        height (int): The height of the button.
        text (str): The text displayed on the button.
        bg_color (tuple): The color of the button.
        text_color (tuple): The color of the text.

    Attributes:
        rect (pygame.Rect): The rectangle representing the button.
        text (str): The text displayed on the button.
        bg_color (tuple): The color of the button.
        text_color (tuple): The color of the text.
        screen (pygame.Surface): The screen to draw the button on.

    Methods:
        draw(): Draw the button on the screen.
        is_clicked(pos): Check if the button is clicked given a mouse position.
        set_bg_color(color): Change the button color.
        set_text_color(color): Change the button text color.
    """
    def __init__(self, screen, x, y, width, height, text, bg_color, text_color):
        """
        Initialize the button

        Args:
            screen (pygame.Surface): the screen to draw on
            x (int): x coordinate of the button
            y (int): y coordinate of the button
            width (int): width of the button
            height (int): height of the button
            text (str): text of the button
            bg_color (tuple): color of the button
            text_color (tuple): color of the text
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.bg_color = bg_color
        self.text_color = text_color
        self.screen = screen

    def draw(self):
        """
        Draw the button on the screen
        """
        pygame.draw.rect(self.screen, self.bg_color, self.rect)
        font = pygame.font.SysFont("", 30)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        """
        Check if the button is clicked given a mouse position

        Args:
            pos (tuple): the position of the mouse

        Returns:
            bool: True if the button is clicked, False otherwise
        """
        return self.rect.collidepoint(pos)

    def set_bg_color(self, color):
        """
        Change the button color

        Args:
            color (tuple): the new color
        """
        self.bg_color = color

    def set_text_color(self, color):
        """
        Change the button text color

        Args:
            color (tuple): the new color
        """
        self.text_color = color
