from pathlib import Path
import sys
import pygame
from pygame import mixer

from build_game import Grid
from constants import LEVEL_MENU_HEIGHT, LEVELS_DIR, MUSIC_DIR, WIDTH, HEIGHT, WHITE, GREEN, RED, BLACK, BLUE, YELLOW, UP, DOWN, LEFT, RIGHT, IMAGES_DIR, HOME, LEVEL, CREATE


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


class SokobanApp:
    def __init__(self, grid_path):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Sokoban")
        self.running = True
        self.page = None
        self.current_level = 0
        # TODO : Centrer les boutons
        self.home_screen_buttons = [
            Button(screen=self.screen, x=50, y=100, width=200, height=50, text="Play", bg_color=GREEN, text_color=BLACK),
            Button(screen=self.screen, x=50, y=200, width=200, height=50, text="Create", bg_color=BLUE, text_color=BLACK),
            Button(screen=self.screen, x=50, y=300, width=200, height=50, text="Quit", bg_color=RED, text_color=BLACK),
        ]
        level_buttons_width = WIDTH // 4
        # TODO : centrer les boutons
        self.level_buttons = [
            Button(screen=self.screen, x=0, y=HEIGHT, width=level_buttons_width, height=LEVEL_MENU_HEIGHT, text="Solve", bg_color=GREEN, text_color=BLACK),
            Button(screen=self.screen, x=level_buttons_width, y=HEIGHT, width=level_buttons_width, height=LEVEL_MENU_HEIGHT, text="Cancel", bg_color=YELLOW, text_color=BLACK),
            Button(screen=self.screen, x=2 * level_buttons_width, y=HEIGHT, width=level_buttons_width, height=LEVEL_MENU_HEIGHT, text="Reset", bg_color=BLUE, text_color=BLACK),
            Button(screen=self.screen, x=3 * level_buttons_width, y=HEIGHT, width=level_buttons_width, height=LEVEL_MENU_HEIGHT, text="Quit", bg_color=RED, text_color=BLACK),
        ]

        # Initialiser le module mixer et charger la musique
        mixer.init()
        self.home_music = mixer.Sound(MUSIC_DIR / "home.mp3")
        self.game_music = mixer.Sound(MUSIC_DIR / "game.mp3")
        self.current_music = None

        self.load_home()

    # LEVEL
    def load_img(self, path):
        return pygame.transform.scale(pygame.image.load(path), (self.cell_width, self.cell_height))

    def draw_cell(self, x, y, img_name):
        self.screen.blit(self.images[img_name], (x * self.cell_width, y * self.cell_height))

    def load_level(self, level_index):
        self.current_level = level_index
        self.page = LEVEL
        self.play_music(self.game_music)
        # TODO : Créer plusieurs niveaux
        grid_path = Path(__file__).parent / "levels" / f"level{level_index}.txt"
        # TODO : enlever la ligne suivante (provisoire)
        grid_path = LEVELS_DIR / f"grid.txt"
        self.grid = Grid(grid_path)
        self.cell_width = WIDTH // self.grid.width
        self.cell_height = HEIGHT // self.grid.height
        pygame.display.set_mode((WIDTH, HEIGHT + LEVEL_MENU_HEIGHT))
        # TODO : Adapted la taille de la fenetre plutot que d'adapter la taille des cellules ??

        self.images = {
            "wall": self.load_img(IMAGES_DIR / "wall.png"),
            "empty_cell": self.load_img(IMAGES_DIR / "empty_cell.png"),
            "box": self.load_img(IMAGES_DIR / "box.png"),
            "goal": self.load_img(IMAGES_DIR / "goal.png"),
            "box_on_goal": self.load_img(IMAGES_DIR / "box_on_goal.png"),
            "player_up": self.load_img(IMAGES_DIR / "player_up.png"),
            "player_down": self.load_img(IMAGES_DIR / "player_down.png"),
            "player_left": self.load_img(IMAGES_DIR / "player_left.png"),
            "player_right": self.load_img(IMAGES_DIR / "player_right.png"),
        }

    def show_level(self):
        self.screen.fill(WHITE)
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                if self.grid.is_empty(x, y):
                    self.draw_cell(x, y, "empty_cell")
                elif self.grid.is_wall(x, y):
                    self.draw_cell(x, y, "wall")
                elif self.grid.is_goal(x, y):
                    self.draw_cell(x, y, "goal")
        
        for box in self.grid.boxes:
            if box.is_on_goal:
                self.draw_cell(box.x, box.y, "box_on_goal")
            else:
                self.draw_cell(box.x, box.y, "box")
        
        if self.grid.player is not None:
            if self.grid.player.orientation == UP:
                self.draw_cell(self.grid.player.x, self.grid.player.y, "player_up")
            elif self.grid.player.orientation == DOWN:
                self.draw_cell(self.grid.player.x, self.grid.player.y, "player_down")
            elif self.grid.player.orientation == LEFT:
                self.draw_cell(self.grid.player.x, self.grid.player.y, "player_left")
            elif self.grid.player.orientation == RIGHT:
                self.draw_cell(self.grid.player.x, self.grid.player.y, "player_right")

        for button in self.level_buttons:
            button.draw()

    def handle_level_event(self, event):
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                self.grid.player.up()
            elif event.key == pygame.K_DOWN:
                self.grid.player.down()
            elif event.key == pygame.K_LEFT:
                self.grid.player.left()
            elif event.key == pygame.K_RIGHT:
                self.grid.player.right()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.level_buttons:
                if button.is_clicked(event.pos):
                    print(button.text)
                    if button.text == "Solve":
                        self.load_solve()
                    if button.text == "Cancel":
                        self.grid.cancel()
                    elif button.text == "Reset":
                        self.grid.reset()
                    elif button.text == "Quit":
                        self.load_home()

    # HOME
    def load_home(self):
        self.page = HOME
        self.play_music(self.home_music)

    def show_home(self):
        # TODO : Ajouter un fond d'ecran
        # TODO : Ajouter un texte
        self.screen.fill(WHITE)

        for button in self.home_screen_buttons:
            button.draw()
    
    def handle_home_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.home_screen_buttons:
                if button.is_clicked(event.pos):
                    if button.text == "Play":
                        self.load_level(self.current_level)
                    elif button.text == "Create":
                        self.load_create()
                    elif button.text == "Quit":
                        self.quit()

    # CREATE
    def load_create(self):
        ...

    def show_create(self):
        ...

    def handle_create_event(self, event):
        ...

    # SOLVE
    def load_solve(self):
        print("SOLVE")

    def show_solve(self):
        ...

    # MAIN
    def play_music(self, music):
        if self.current_music is not None:
            self.current_music.stop()
        music.play(-1)
        self.current_music = music

    def stop_music(self):
        if self.current_music is not None:
            self.current_music.stop()
            self.current_music = None

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.quit()
        elif self.page == HOME:
            self.handle_home_event(event)
        elif self.page == CREATE:
            self.handle_create_event(event)
        elif self.page == LEVEL:
            self.handle_level_event(event)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)

            if self.page == HOME:
                self.show_home()
            elif self.page == CREATE:
                self.show_create()
            elif self.page == LEVEL:
                self.show_level()
            
            pygame.display.flip()

    def quit(self):
        self.running = False
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    grid_path = Path(__file__).resolve().parent / "grid" / "grid.txt"
    app = SokobanApp(grid_path)
    app.run()
